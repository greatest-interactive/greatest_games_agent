"""
Data export service for CSV and JSON formats
"""
import csv
import json
from io import StringIO
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class DataExportService:
    """Service to handle data exports in various formats"""
    
    @staticmethod
    def export_payments_csv(user, days=30):
        """Export user's payments as CSV"""
        from api.models import Payment
        from django.utils import timezone
        
        since = timezone.now() - timezone.timedelta(days=days)
        payments = Payment.objects.filter(
            user=user,
            created_at__gte=since
        ).select_related('tier').order_by('-created_at')
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header row
        writer.writerow([
            'Payment Date',
            'Amount',
            'Currency',
            'Tier',
            'Billing Period',
            'Status',
            'Stripe Charge ID',
            'Description'
        ])
        
        # Data rows
        for payment in payments:
            writer.writerow([
                payment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                payment.amount,
                payment.currency,
                payment.tier.display_name if payment.tier else 'N/A',
                payment.billing_period,
                payment.status,
                payment.stripe_charge_id or '',
                payment.description or ''
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_payments_json(user, days=30):
        """Export user's payments as JSON"""
        from api.models import Payment
        from django.utils import timezone
        
        since = timezone.now() - timezone.timedelta(days=days)
        payments = Payment.objects.filter(
            user=user,
            created_at__gte=since
        ).select_related('tier').order_by('-created_at')
        
        data = {
            'export_date': datetime.now().isoformat(),
            'user': user.username,
            'period_days': days,
            'total_records': payments.count(),
            'payments': []
        }
        
        for payment in payments:
            data['payments'].append({
                'id': payment.id,
                'date': payment.created_at.isoformat(),
                'amount': str(payment.amount),
                'currency': payment.currency,
                'tier': payment.tier.display_name if payment.tier else None,
                'billing_period': payment.billing_period,
                'status': payment.status,
                'stripe_charge_id': payment.stripe_charge_id,
                'description': payment.description
            })
        
        return json.dumps(data, indent=2)
    
    @staticmethod
    def export_invoices_csv(user, days=30):
        """Export user's invoices as CSV"""
        from api.models import Invoice
        from django.utils import timezone
        
        since = timezone.now() - timezone.timedelta(days=days)
        invoices = Invoice.objects.filter(
            user=user,
            created_at__gte=since
        ).select_related('payment', 'payment__tier').order_by('-created_at')
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header row
        writer.writerow([
            'Invoice Date',
            'Invoice ID',
            'Amount',
            'Currency',
            'Tier',
            'Status',
            'Billing Period',
            'Due Date',
            'Payment Method'
        ])
        
        # Data rows
        for invoice in invoices:
            writer.writerow([
                invoice.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                invoice.id,
                invoice.amount,
                invoice.currency,
                invoice.payment.tier.display_name if invoice.payment and invoice.payment.tier else 'N/A',
                invoice.status,
                invoice.billing_period,
                invoice.due_date.strftime('%Y-%m-%d') if invoice.due_date else '',
                invoice.payment_method or ''
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_invoices_json(user, days=30):
        """Export user's invoices as JSON"""
        from api.models import Invoice
        from django.utils import timezone
        
        since = timezone.now() - timezone.timedelta(days=days)
        invoices = Invoice.objects.filter(
            user=user,
            created_at__gte=since
        ).select_related('payment', 'payment__tier').order_by('-created_at')
        
        data = {
            'export_date': datetime.now().isoformat(),
            'user': user.username,
            'period_days': days,
            'total_records': invoices.count(),
            'invoices': []
        }
        
        for invoice in invoices:
            data['invoices'].append({
                'id': invoice.id,
                'date': invoice.created_at.isoformat(),
                'amount': str(invoice.amount),
                'currency': invoice.currency,
                'tier': invoice.payment.tier.display_name if invoice.payment and invoice.payment.tier else None,
                'status': invoice.status,
                'billing_period': invoice.billing_period,
                'due_date': invoice.due_date.isoformat() if invoice.due_date else None,
                'payment_method': invoice.payment_method
            })
        
        return json.dumps(data, indent=2)
    
    @staticmethod
    def export_analytics_csv(user, days=30, event_type=None):
        """Export user's analytics events as CSV"""
        from api.models import AnalyticsEvent
        from django.utils import timezone
        
        since = timezone.now() - timezone.timedelta(days=days)
        events = AnalyticsEvent.objects.filter(
            user=user,
            created_at__gte=since
        ).order_by('-created_at')
        
        if event_type:
            events = events.filter(event_type=event_type)
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header row
        writer.writerow([
            'Date',
            'Event Type',
            'Event Name',
            'Page',
            'Duration (seconds)',
            'Session ID',
            'Metadata'
        ])
        
        # Data rows
        for event in events:
            writer.writerow([
                event.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                event.get_event_type_display(),
                event.event_name,
                event.page or '',
                event.duration_seconds or '',
                event.session_id or '',
                json.dumps(event.metadata) if event.metadata else ''
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_analytics_json(user, days=30, event_type=None):
        """Export user's analytics events as JSON"""
        from api.models import AnalyticsEvent
        from django.utils import timezone
        
        since = timezone.now() - timezone.timedelta(days=days)
        events = AnalyticsEvent.objects.filter(
            user=user,
            created_at__gte=since
        ).order_by('-created_at')
        
        if event_type:
            events = events.filter(event_type=event_type)
        
        data = {
            'export_date': datetime.now().isoformat(),
            'user': user.username,
            'period_days': days,
            'event_type_filter': event_type,
            'total_records': events.count(),
            'events': []
        }
        
        for event in events:
            data['events'].append({
                'id': event.id,
                'date': event.created_at.isoformat(),
                'event_type': event.event_type,
                'event_type_display': event.get_event_type_display(),
                'event_name': event.event_name,
                'page': event.page,
                'duration_seconds': event.duration_seconds,
                'session_id': event.session_id,
                'metadata': event.metadata
            })
        
        return json.dumps(data, indent=2)
    
    @staticmethod
    def export_user_data_csv(user):
        """Export comprehensive user data as CSV"""
        from api.models import UserSubscription
        
        output = StringIO()
        writer = csv.writer(output)
        
        # User Info Section
        writer.writerow(['USER INFORMATION'])
        writer.writerow(['Username', user.username])
        writer.writerow(['Email', user.email])
        writer.writerow(['First Name', user.first_name])
        writer.writerow(['Last Name', user.last_name])
        writer.writerow(['Date Joined', user.date_joined.strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        
        # Subscription Info
        try:
            subscription = user.subscription
            writer.writerow(['SUBSCRIPTION INFORMATION'])
            writer.writerow(['Tier', subscription.tier.display_name if subscription.tier else 'Free'])
            writer.writerow(['Status', subscription.status])
            writer.writerow(['Monthly Tokens', subscription.tier.monthly_tokens if subscription.tier else 0])
            writer.writerow(['Tokens Used This Month', subscription.tokens_used_this_month])
            writer.writerow(['Renewal Date', subscription.renewal_date.strftime('%Y-%m-%d') if subscription.renewal_date else 'N/A'])
            writer.writerow([])
        except:
            pass
        
        return output.getvalue()
    
    @staticmethod
    def export_user_data_json(user):
        """Export comprehensive user data as JSON"""
        from api.models import UserSubscription
        
        data = {
            'export_date': datetime.now().isoformat(),
            'user': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined.isoformat()
            }
        }
        
        # Add subscription info
        try:
            subscription = user.subscription
            data['subscription'] = {
                'tier': subscription.tier.display_name if subscription.tier else 'Free',
                'tier_name': subscription.tier.name if subscription.tier else 'free',
                'status': subscription.status,
                'monthly_tokens': subscription.tier.monthly_tokens if subscription.tier else 0,
                'tokens_used_this_month': subscription.tokens_used_this_month,
                'renewal_date': subscription.renewal_date.isoformat() if subscription.renewal_date else None
            }
        except:
            data['subscription'] = None
        
        return json.dumps(data, indent=2)
