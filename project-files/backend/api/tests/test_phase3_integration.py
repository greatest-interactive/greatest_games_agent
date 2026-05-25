"""
End-to-End Integration Tests for Phase 3 Features

Tests Phase 3 model functionality and integrations:
1. User and profile creation
2. Tier selection and management
3. Payment processing
4. Invoice generation
5. Webhook event handling
6. Analytics tracking
7. User subscription tracking
8. Data model integrity and relationships
"""

from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
from decimal import Decimal

from api.models import (
    UserProfile, Tier, UserSubscription, Payment, Invoice, 
    AnalyticsEvent, WebhookEvent
)


class Phase3ModelIntegrationTest(TestCase):
    """Integration tests for Phase 3 model functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create tiers
        self.free_tier = Tier.objects.create(
            name='free',
            display_name='Free',
            description='Free tier for getting started',
            price_monthly=0,
            monthly_tokens=1000,
            max_api_requests_per_day=100,
            features=['Dashboard', 'Basic Analysis']
        )
        
        self.pro_tier = Tier.objects.create(
            name='pro',
            display_name='Pro',
            description='Pro tier with advanced features',
            price_monthly=29.99,
            monthly_tokens=10000,
            max_api_requests_per_day=1000,
            features=['Dashboard', 'Advanced Analysis', 'API Access']
        )
        
        self.enterprise_tier = Tier.objects.create(
            name='enterprise',
            display_name='Enterprise',
            description='Enterprise tier with unlimited features',
            price_monthly=99.99,
            monthly_tokens=999999,
            max_api_requests_per_day=999999,
            features=['Dashboard', 'Advanced Analysis', 'API Access', 'Priority Support']
        )
    
    def test_01_user_and_profile_creation(self):
        """Test 1: User creation with profile"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        profile = UserProfile.objects.create(user=user, role='user')
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(profile.role, 'user')
        self.assertTrue(hasattr(user, 'profile'))
    
    def test_02_tier_creation_and_retrieval(self):
        """Test 2: Tier creation with proper fields"""
        tier = Tier.objects.get(name='pro')
        
        self.assertEqual(tier.display_name, 'Pro')
        self.assertEqual(tier.price_monthly, Decimal('29.99'))
        self.assertEqual(tier.monthly_tokens, 10000)
        self.assertEqual(tier.max_api_requests_per_day, 1000)
    
    def test_03_user_subscription_creation(self):
        """Test 3: User subscription to tier"""
        user = User.objects.create_user(
            username='subuser',
            email='sub@example.com',
            password='SecurePass123!'
        )
        UserProfile.objects.create(user=user)
        
        subscription = UserSubscription.objects.create(
            user=user,
            tier=self.pro_tier,
            is_active=True,
            payment_method='stripe'
        )
        
        self.assertEqual(subscription.tier, self.pro_tier)
        self.assertTrue(subscription.is_active)
    
    def test_04_payment_creation_and_status(self):
        """Test 4: Payment creation with proper fields"""
        user = User.objects.create_user(
            username='payuser',
            email='pay@example.com',
            password='SecurePass123!'
        )
        UserProfile.objects.create(user=user)
        
        payment = Payment.objects.create(
            user=user,
            stripe_charge_id='ch_test123',
            amount=2999,
            currency='USD',
            status='completed',
            tier=self.pro_tier,
            billing_period='monthly'
        )
        
        self.assertEqual(payment.status, 'completed')
        self.assertEqual(payment.amount, 2999)
        self.assertEqual(payment.stripe_charge_id, 'ch_test123')
    
    def test_05_invoice_generation_flow(self):
        """Test 5: Invoice generation after payment"""
        user = User.objects.create_user(
            username='invuser',
            email='inv@example.com',
            password='SecurePass123!'
        )
        UserProfile.objects.create(user=user)
        
        payment = Payment.objects.create(
            user=user,
            stripe_charge_id='ch_inv_001',
            amount=2999,
            currency='USD',
            status='completed',
            tier=self.pro_tier,
            billing_period='monthly'
        )
        
        today = date.today()
        invoice = Invoice.objects.create(
            user=user,
            payment=payment,
            amount=2999,
            currency='USD',
            status='paid',
            invoice_number=f'INV-{user.id}-001',
            billing_period_start=today,
            billing_period_end=today,
            due_date=today + timedelta(days=30)
        )
        
        self.assertEqual(invoice.status, 'paid')
        self.assertEqual(invoice.payment, payment)
    
    def test_06_webhook_event_creation(self):
        """Test 6: Webhook event processing and storage"""
        user = User.objects.create_user(
            username='webhookuser',
            email='webhook@example.com',
            password='SecurePass123!'
        )
        UserProfile.objects.create(user=user)
        
        payment = Payment.objects.create(
            user=user,
            stripe_charge_id='ch_webhook_001',
            amount=2999,
            currency='USD',
            status='pending',
            tier=self.pro_tier,
            billing_period='monthly'
        )
        
        webhook_event = WebhookEvent.objects.create(
            stripe_event_id='evt_test_001',
            event_type='charge.succeeded',
            api_version='2023-10-16',
            status='succeeded',
            user=user,
            payment=payment,
            raw_data={'id': 'evt_test_001', 'type': 'charge.succeeded'}
        )
        
        self.assertEqual(webhook_event.status, 'succeeded')
        self.assertEqual(webhook_event.event_type, 'charge.succeeded')
    
    def test_07_webhook_deduplication(self):
        """Test 7: Webhook events are deduplicated"""
        user = User.objects.create_user(
            username='dedupuser',
            email='dedup@example.com',
            password='SecurePass123!'
        )
        UserProfile.objects.create(user=user)
        
        payment = Payment.objects.create(
            user=user,
            stripe_charge_id='ch_dedup_001',
            amount=2999,
            currency='USD',
            status='pending',
            tier=self.pro_tier,
            billing_period='monthly'
        )
        
        # Create first webhook event
        event1 = WebhookEvent.objects.create(
            stripe_event_id='evt_dedup_001',
            event_type='charge.succeeded',
            api_version='2023-10-16',
            status='succeeded',
            user=user,
            payment=payment,
            raw_data={'test': 'data'}
        )
        
        # Try to create duplicate using get_or_create
        event2, created = WebhookEvent.objects.get_or_create(
            stripe_event_id='evt_dedup_001',
            defaults={
                'event_type': 'charge.succeeded',
                'api_version': '2023-10-16',
                'status': 'succeeded',
                'user': user,
                'payment': payment,
                'raw_data': {'test': 'data'}
            }
        )
        
        self.assertFalse(created)  # Should not create new
        self.assertEqual(event1.id, event2.id)  # Should return same event
    
    def test_08_analytics_event_creation(self):
        """Test 8: Analytics event tracking"""
        user = User.objects.create_user(
            username='analyticsuser',
            email='analytics@example.com',
            password='SecurePass123!'
        )
        UserProfile.objects.create(user=user)
        
        event = AnalyticsEvent.objects.create(
            user=user,
            event_type='purchase',
            event_name='Pro Tier Upgrade',
            page='billing',
            metadata={'tier': 'pro', 'amount': 2999}
        )
        
        self.assertEqual(event.event_type, 'purchase')
        self.assertEqual(event.user, user)
    
    def test_09_complete_payment_flow(self):
        """Test 9: Complete payment flow integration"""
        # Create user
        user = User.objects.create_user(
            username='flowuser',
            email='flow@example.com',
            password='SecurePass123!'
        )
        profile = UserProfile.objects.create(user=user, role='user')
        
        # Create subscription
        subscription = UserSubscription.objects.create(
            user=user,
            tier=self.free_tier,
            is_active=True,
            payment_method='free'
        )
        
        # Log upgrade analytics
        AnalyticsEvent.objects.create(
            user=user,
            event_type='tier_upgrade',
            event_name='Upgrading to Pro',
            page='billing',
            metadata={'from': 'free', 'to': 'pro'}
        )
        
        # Create payment
        payment = Payment.objects.create(
            user=user,
            stripe_charge_id='ch_flow_001',
            amount=2999,
            currency='USD',
            status='completed',
            tier=self.pro_tier,
            billing_period='monthly'
        )
        
        # Generate invoice
        today = date.today()
        invoice = Invoice.objects.create(
            user=user,
            payment=payment,
            amount=2999,
            currency='USD',
            status='paid',
            invoice_number=f'INV-FLOW-{user.id}',
            billing_period_start=today,
            billing_period_end=today,
            due_date=today + timedelta(days=30)
        )
        
        # Process webhook
        webhook = WebhookEvent.objects.create(
            stripe_event_id='evt_flow_001',
            event_type='charge.succeeded',
            api_version='2023-10-16',
            status='succeeded',
            user=user,
            payment=payment,
            raw_data={'charge_id': 'ch_flow_001'}
        )
        
        # Verify all relationships
        self.assertEqual(subscription.user, user)
        self.assertEqual(payment.user, user)
        self.assertEqual(invoice.payment, payment)
        self.assertEqual(webhook.payment, payment)
    
    def test_10_multiple_payments_per_user(self):
        """Test 10: User can have multiple payments"""
        user = User.objects.create_user(
            username='multiuser',
            email='multi@example.com',
            password='SecurePass123!'
        )
        UserProfile.objects.create(user=user)
        
        # Create multiple payments
        payment1 = Payment.objects.create(
            user=user,
            stripe_charge_id='ch_multi_001',
            amount=2999,
            currency='USD',
            status='completed',
            tier=self.pro_tier,
            billing_period='monthly'
        )
        
        payment2 = Payment.objects.create(
            user=user,
            stripe_charge_id='ch_multi_002',
            amount=9999,
            currency='USD',
            status='completed',
            tier=self.enterprise_tier,
            billing_period='yearly'
        )
        
        user_payments = Payment.objects.filter(user=user)
        self.assertEqual(user_payments.count(), 2)
    
    def test_11_subscription_status_updates(self):
        """Test 11: Subscription status can be updated"""
        user = User.objects.create_user(
            username='statususer',
            email='status@example.com',
            password='SecurePass123!'
        )
        UserProfile.objects.create(user=user)
        
        subscription = UserSubscription.objects.create(
            user=user,
            tier=self.pro_tier,
            is_active=True,
            payment_method='stripe'
        )
        
        # Deactivate subscription
        subscription.is_active = False
        subscription.save()
        
        refreshed = UserSubscription.objects.get(user=user)
        self.assertFalse(refreshed.is_active)
    
    def test_12_webhook_retry_tracking(self):
        """Test 12: Webhook retry count tracking"""
        user = User.objects.create_user(
            username='retryuser',
            email='retry@example.com',
            password='SecurePass123!'
        )
        UserProfile.objects.create(user=user)
        
        payment = Payment.objects.create(
            user=user,
            stripe_charge_id='ch_retry_001',
            amount=2999,
            currency='USD',
            status='pending',
            tier=self.pro_tier,
            billing_period='monthly'
        )
        
        webhook = WebhookEvent.objects.create(
            stripe_event_id='evt_retry_001',
            event_type='charge.failed',
            api_version='2023-10-16',
            status='failed',
            user=user,
            payment=payment,
            raw_data={},
            retry_count=2,
            error_message='Connection timeout'
        )
        
        self.assertEqual(webhook.retry_count, 2)
        self.assertEqual(webhook.status, 'failed')
    
    def test_13_tier_features_list(self):
        """Test 13: Tier features are stored correctly"""
        tier = Tier.objects.get(name='enterprise')
        
        self.assertIn('Priority Support', tier.features)
        self.assertEqual(len(tier.features), 4)
    
    def test_14_complete_journey_validation(self):
        """Test 14: Complete end-to-end journey"""
        # 1. Create user
        user = User.objects.create_user(
            username='journeyuser',
            email='journey@example.com',
            password='SecurePass123!'
        )
        UserProfile.objects.create(user=user, role='user')
        
        # 2. Create free subscription
        sub1 = UserSubscription.objects.create(
            user=user,
            tier=self.free_tier,
            is_active=True,
            payment_method='free'
        )
        
        # 3. Record upgrade decision
        AnalyticsEvent.objects.create(
            user=user,
            event_type='page_view',
            event_name='Pricing Page View',
            page='pricing',
            metadata={}
        )
        
        # 4. Create payment for upgrade
        payment = Payment.objects.create(
            user=user,
            stripe_charge_id='ch_journey_001',
            amount=2999,
            currency='USD',
            status='completed',
            tier=self.pro_tier,
            billing_period='monthly'
        )
        
        # 5. Generate invoice
        today = date.today()
        invoice = Invoice.objects.create(
            user=user,
            payment=payment,
            amount=2999,
            currency='USD',
            status='paid',
            invoice_number=f'INV-JOURNEY-{user.id}',
            billing_period_start=today,
            billing_period_end=today,
            due_date=today + timedelta(days=30)
        )
        
        # 6. Process webhook confirmation
        webhook = WebhookEvent.objects.create(
            stripe_event_id='evt_journey_001',
            event_type='charge.succeeded',
            api_version='2023-10-16',
            status='succeeded',
            user=user,
            payment=payment,
            raw_data={'confirmed': True}
        )
        
        # 7. Update subscription
        sub1.tier = self.pro_tier
        sub1.save()
        
        # 8. Log conversion
        AnalyticsEvent.objects.create(
            user=user,
            event_type='purchase',
            event_name='Successful Pro Upgrade',
            page='billing',
            metadata={'tier': 'pro', 'payment_id': payment.id}
        )
        
        # Verify all objects exist and are linked
        self.assertEqual(Payment.objects.filter(user=user).count(), 1)
        self.assertEqual(Invoice.objects.filter(user=user).count(), 1)
        self.assertEqual(WebhookEvent.objects.filter(user=user).count(), 1)
        self.assertEqual(AnalyticsEvent.objects.filter(user=user).count(), 2)
        
        # Verify relationships
        self.assertEqual(invoice.payment, payment)
        self.assertEqual(webhook.payment, payment)
