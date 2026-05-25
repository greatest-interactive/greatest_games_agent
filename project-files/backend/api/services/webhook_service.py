"""
Stripe Webhook Service
Handles webhook signature validation and event processing
"""
import stripe
import json
import hmac
import hashlib
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from api.models import WebhookEvent, Payment, User


class StripeWebhookHandler:
    """Handle incoming Stripe webhooks with signature validation"""
    
    def __init__(self):
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        self.event_handlers = {
            'payment_intent.succeeded': self.handle_payment_intent_succeeded,
            'payment_intent.payment_failed': self.handle_payment_intent_failed,
            'customer.subscription.updated': self.handle_subscription_updated,
            'customer.subscription.deleted': self.handle_subscription_deleted,
            'invoice.paid': self.handle_invoice_paid,
            'invoice.payment_failed': self.handle_invoice_payment_failed,
        }
    
    def validate_signature(self, payload, signature):
        """
        Validate Stripe webhook signature
        
        Args:
            payload: Raw request body (bytes)
            signature: Stripe-Signature header value
            
        Returns:
            dict: Parsed event data if valid, None if invalid
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            return event
        except ValueError:
            # Invalid payload
            return None
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return None
    
    def process_event(self, event):
        """
        Process a validated Stripe webhook event
        
        Args:
            event: Stripe webhook event
            
        Returns:
            dict: Processing result
        """
        event_type = event.get('type')
        stripe_event_id = event.get('id')
        
        # Check if event already processed
        existing_event = WebhookEvent.objects.filter(
            stripe_event_id=stripe_event_id
        ).first()
        
        if existing_event:
            return {
                'success': True,
                'message': 'Event already processed',
                'event_id': stripe_event_id
            }
        
        # Create webhook event record
        webhook_event = WebhookEvent.objects.create(
            stripe_event_id=stripe_event_id,
            event_type=event_type,
            api_version=event.get('api_version'),
            raw_data=event,
            status='processing'
        )
        
        try:
            # Route to appropriate handler
            handler = self.event_handlers.get(event_type)
            
            if handler:
                result = handler(event, webhook_event)
                webhook_event.status = 'succeeded'
                webhook_event.processed_at = timezone.now()
                webhook_event.save()
                return result
            else:
                # Unknown event type - just log it
                webhook_event.status = 'ignored'
                webhook_event.processed_at = timezone.now()
                webhook_event.save()
                return {
                    'success': True,
                    'message': f'Event type {event_type} not handled',
                    'event_id': stripe_event_id
                }
        
        except Exception as e:
            webhook_event.status = 'failed'
            webhook_event.error_message = str(e)
            webhook_event.retry_count += 1
            webhook_event.save()
            return {
                'success': False,
                'message': f'Error processing event: {str(e)}',
                'event_id': stripe_event_id
            }
    
    def handle_payment_intent_succeeded(self, event, webhook_event):
        """Handle successful payment intent"""
        payment_intent = event.get('data', {}).get('object', {})
        stripe_payment_intent_id = payment_intent.get('id')
        
        try:
            # Find related payment record
            payment = Payment.objects.filter(
                stripe_payment_intent_id=stripe_payment_intent_id
            ).first()
            
            if payment:
                payment.status = 'succeeded'
                payment.stripe_payment_method_id = payment_intent.get('payment_method')
                payment.save()
                webhook_event.payment = payment
                webhook_event.user = payment.user
                webhook_event.save()
                
                return {
                    'success': True,
                    'message': f'Payment {stripe_payment_intent_id} succeeded',
                    'event_id': event.get('id')
                }
            else:
                return {
                    'success': False,
                    'message': f'Payment {stripe_payment_intent_id} not found',
                    'event_id': event.get('id')
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error handling payment succeeded: {str(e)}',
                'event_id': event.get('id')
            }
    
    def handle_payment_intent_failed(self, event, webhook_event):
        """Handle failed payment intent"""
        payment_intent = event.get('data', {}).get('object', {})
        stripe_payment_intent_id = payment_intent.get('id')
        
        try:
            # Find related payment record
            payment = Payment.objects.filter(
                stripe_payment_intent_id=stripe_payment_intent_id
            ).first()
            
            if payment:
                payment.status = 'failed'
                payment.save()
                webhook_event.payment = payment
                webhook_event.user = payment.user
                webhook_event.save()
                
                # TODO: Send failure email notification
                
                return {
                    'success': True,
                    'message': f'Payment {stripe_payment_intent_id} failed',
                    'event_id': event.get('id')
                }
            else:
                return {
                    'success': False,
                    'message': f'Payment {stripe_payment_intent_id} not found',
                    'event_id': event.get('id')
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error handling payment failed: {str(e)}',
                'event_id': event.get('id')
            }
    
    def handle_subscription_updated(self, event, webhook_event):
        """Handle subscription update"""
        subscription = event.get('data', {}).get('object', {})
        customer_id = subscription.get('customer')
        
        try:
            # Subscription update handled separately, just log it
            return {
                'success': True,
                'message': f'Subscription {subscription.get("id")} updated',
                'event_id': event.get('id')
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error handling subscription update: {str(e)}',
                'event_id': event.get('id')
            }
    
    def handle_subscription_deleted(self, event, webhook_event):
        """Handle subscription cancellation"""
        subscription = event.get('data', {}).get('object', {})
        
        try:
            # Subscription deletion handled separately, just log it
            return {
                'success': True,
                'message': f'Subscription {subscription.get("id")} deleted',
                'event_id': event.get('id')
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error handling subscription deletion: {str(e)}',
                'event_id': event.get('id')
            }
    
    def handle_invoice_paid(self, event, webhook_event):
        """Handle paid invoice"""
        invoice = event.get('data', {}).get('object', {})
        
        try:
            # Invoice paid event
            return {
                'success': True,
                'message': f'Invoice {invoice.get("id")} paid',
                'event_id': event.get('id')
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error handling invoice paid: {str(e)}',
                'event_id': event.get('id')
            }
    
    def handle_invoice_payment_failed(self, event, webhook_event):
        """Handle failed invoice payment"""
        invoice = event.get('data', {}).get('object', {})
        
        try:
            # Invoice payment failed event
            return {
                'success': True,
                'message': f'Invoice {invoice.get("id")} payment failed',
                'event_id': event.get('id')
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error handling invoice payment failed: {str(e)}',
                'event_id': event.get('id')
            }


class WebhookRetryManager:
    """Manage webhook retry logic"""
    
    @staticmethod
    def get_failed_events():
        """Get webhook events that failed and need retry"""
        # Get events that failed in the last 24 hours with less than 5 retries
        hours_24_ago = timezone.now() - timedelta(hours=24)
        
        return WebhookEvent.objects.filter(
            status='failed',
            retry_count__lt=5,
            received_at__gte=hours_24_ago
        ).order_by('retry_count')
    
    @staticmethod
    def retry_event(webhook_event):
        """Retry processing a failed webhook event"""
        handler = StripeWebhookHandler()
        result = handler.process_event(webhook_event.raw_data)
        return result
