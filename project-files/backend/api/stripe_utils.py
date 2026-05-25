"""
Stripe payment processing utilities
"""
import stripe
import os
from decimal import Decimal
from django.conf import settings
from datetime import datetime, timedelta
from .models import Payment, Invoice, Tier, User
import uuid

# Initialize Stripe with API key
# Use test keys for development, production keys in settings
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_51234567890123456789')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_1234567890123456789')

stripe.api_key = STRIPE_SECRET_KEY


class StripePaymentProcessor:
    """Handle all Stripe payment operations"""
    
    @staticmethod
    def create_payment_intent(user, tier, billing_period='monthly'):
        """
        Create a Stripe PaymentIntent for subscription upgrade
        
        Args:
            user: User object
            tier: Tier object (Starter, Pro, Enterprise)
            billing_period: 'monthly' or 'yearly'
        
        Returns:
            dict with client_secret and payment_intent_id
        """
        if not tier or tier.name == 'free':
            raise ValueError("Cannot create payment for free tier")
        
        # Determine amount
        if billing_period == 'yearly' and tier.price_yearly:
            amount = tier.price_yearly
        else:
            amount = tier.price_monthly
        
        # Convert to cents for Stripe
        amount_cents = int(amount * 100)
        
        try:
            # Create or get Stripe customer
            customer = StripePaymentProcessor.get_or_create_customer(user)
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='usd',
                customer=customer['id'],
                metadata={
                    'user_id': user.id,
                    'username': user.username,
                    'tier': tier.name,
                    'billing_period': billing_period,
                },
                description=f"{user.username} - {tier.display_name} ({billing_period})"
            )
            
            return {
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'amount': float(amount),
                'currency': 'USD',
                'tier': tier.name,
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe payment intent error: {str(e)}")
    
    @staticmethod
    def get_or_create_customer(user):
        """Get or create a Stripe customer for user"""
        try:
            # Check if user already has Stripe customer ID
            if hasattr(user, 'subscription') and user.subscription.tier:
                # Try to retrieve existing customer
                customers = stripe.Customer.list(email=user.email, limit=1)
                if customers and len(customers.data) > 0:
                    return customers.data[0]
            
            # Create new customer
            customer = stripe.Customer.create(
                email=user.email,
                name=f"{user.first_name} {user.last_name}".strip(),
                metadata={'user_id': user.id}
            )
            return customer
        except stripe.error.StripeError as e:
            raise Exception(f"Error managing Stripe customer: {str(e)}")
    
    @staticmethod
    def confirm_payment(payment_intent_id, tier, billing_period='monthly'):
        """
        Confirm a payment and upgrade user subscription
        
        Args:
            payment_intent_id: Stripe PaymentIntent ID
            tier: Tier object to upgrade to
            billing_period: 'monthly' or 'yearly'
        
        Returns:
            Payment object
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status != 'succeeded':
                raise Exception(f"Payment intent status is {intent.status}, not succeeded")
            
            user_id = intent.metadata.get('user_id')
            user = User.objects.get(id=user_id)
            
            # Create payment record
            amount = Decimal(str(intent.amount / 100))  # Convert cents back to dollars
            
            payment = Payment.objects.create(
                user=user,
                stripe_charge_id=intent.charges.data[0].id if intent.charges.data else payment_intent_id,
                stripe_customer_id=intent.customer,
                amount=amount,
                tier=tier,
                billing_period=billing_period,
                status='completed',
                completed_at=datetime.now(),
                description=f"Subscription upgrade to {tier.display_name}"
            )
            
            # Create invoice
            invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
            billing_start = datetime.now().date()
            if billing_period == 'yearly':
                billing_end = billing_start + timedelta(days=365)
            else:
                billing_end = billing_start + timedelta(days=30)
            
            invoice = Invoice.objects.create(
                user=user,
                payment=payment,
                invoice_number=invoice_number,
                stripe_invoice_id=intent.id,
                tier=tier,
                amount=amount,
                billing_period_start=billing_start,
                billing_period_end=billing_end,
                due_date=billing_end,
                status='paid'
            )
            
            # Update user subscription
            from .models import UserSubscription
            subscription, created = UserSubscription.objects.get_or_create(user=user)
            subscription.tier = tier
            subscription.payment_method = 'stripe'
            subscription.is_active = True
            subscription.started_at = datetime.now()
            
            if billing_period == 'yearly':
                subscription.expires_at = datetime.now() + timedelta(days=365)
                subscription.renewal_date = (datetime.now() + timedelta(days=365)).date()
            else:
                subscription.expires_at = datetime.now() + timedelta(days=30)
                subscription.renewal_date = (datetime.now() + timedelta(days=30)).date()
            
            subscription.save()
            
            return payment
            
        except stripe.error.StripeError as e:
            raise Exception(f"Error confirming payment: {str(e)}")
        except User.DoesNotExist:
            raise Exception("User not found for payment")
    
    @staticmethod
    def create_refund(payment_id, amount=None):
        """Create a Stripe refund"""
        try:
            payment = Payment.objects.get(id=payment_id)
            
            refund_amount = None
            if amount:
                refund_amount = int(amount * 100)  # Convert to cents
            
            refund = stripe.Refund.create(
                charge=payment.stripe_charge_id,
                amount=refund_amount,
                metadata={'payment_id': payment_id}
            )
            
            # Update payment status
            payment.status = 'refunded'
            payment.save()
            
            return refund
        except stripe.error.StripeError as e:
            raise Exception(f"Error creating refund: {str(e)}")
    
    @staticmethod
    def validate_webhook_signature(payload, signature):
        """Validate Stripe webhook signature"""
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', '')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            return event
        except ValueError as e:
            raise Exception(f"Invalid webhook payload: {str(e)}")
        except stripe.error.SignatureVerificationError as e:
            raise Exception(f"Invalid webhook signature: {str(e)}")
    
    @staticmethod
    def process_tier_upgrade(user, from_tier, to_tier, billing_period='monthly'):
        """
        Process a tier upgrade/downgrade with prorated credit
        
        Args:
            user: User object
            from_tier: Current Tier object
            to_tier: New Tier object
            billing_period: 'monthly' or 'yearly'
        
        Returns:
            dict with upgrade details and payment intent
        """
        from .models import TierChange, UserSubscription
        
        if not to_tier or to_tier.name == 'free':
            raise ValueError("Cannot upgrade to free tier via payment")
        
        # Get or create subscription
        subscription, _ = UserSubscription.objects.get_or_create(user=user)
        
        # Calculate prorated credit from current tier
        prorated_credit = Decimal('0')
        change_type = 'upgrade'
        
        if from_tier and from_tier.price_monthly and from_tier != to_tier:
            # Calculate days remaining in current billing period
            if subscription.renewal_date:
                days_remaining = (subscription.renewal_date - datetime.now().date()).days
                if days_remaining > 0:
                    daily_rate = from_tier.price_monthly / Decimal('30')
                    prorated_credit = daily_rate * Decimal(str(days_remaining))
            
            # Determine change type
            if from_tier.price_monthly > to_tier.price_monthly:
                change_type = 'downgrade'
            else:
                change_type = 'upgrade'
        else:
            change_type = 'upgrade'
        
        # Calculate new tier amount
        if billing_period == 'yearly' and to_tier.price_yearly:
            amount = to_tier.price_yearly
        else:
            amount = to_tier.price_monthly
        
        # Apply prorated credit
        amount_due = amount - prorated_credit
        if amount_due < 0:
            amount_due = Decimal('0')
        
        # Create payment intent if amount due
        payment_intent_data = None
        payment = None
        
        if amount_due > 0:
            payment_intent_data = StripePaymentProcessor.create_payment_intent(
                user, to_tier, billing_period
            )
            
            # Create Payment record
            payment = Payment.objects.create(
                user=user,
                stripe_charge_id=payment_intent_data.get('payment_intent_id'),
                amount=amount_due,
                tier=to_tier,
                billing_period=billing_period,
                status='pending',
                description=f'Tier upgrade/downgrade: {from_tier.display_name if from_tier else "Free"} → {to_tier.display_name}'
            )
        
        # Create TierChange record
        tier_change = TierChange.objects.create(
            user=user,
            from_tier=from_tier,
            to_tier=to_tier,
            change_type=change_type,
            payment=payment,
            billing_period=billing_period,
            amount_charged=amount_due,
            prorated_credit=prorated_credit,
            status='pending' if amount_due > 0 else 'completed'
        )
        
        # If no payment needed, immediately apply tier change
        if amount_due <= 0:
            subscription.tier = to_tier
            subscription.started_at = datetime.now()
            subscription.renewal_date = (datetime.now() + timedelta(days=30 if billing_period == 'monthly' else 365)).date()
            subscription.save()
            tier_change.status = 'completed'
            tier_change.save()
        
        return {
            'tier_change_id': tier_change.id,
            'change_type': change_type,
            'from_tier': from_tier.display_name if from_tier else 'Free',
            'to_tier': to_tier.display_name,
            'prorated_credit': float(prorated_credit),
            'amount_due': float(amount_due),
            'payment_intent': payment_intent_data,
            'status': tier_change.status
        }
