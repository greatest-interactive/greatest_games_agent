"""
API views for payment processing, invoices, and analytics
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from decimal import Decimal

from .models import (
    Payment, Invoice, AnalyticsEvent, Tier, UserSubscription, WebhookEvent
)
from .serializers import (
    PaymentSerializer, InvoiceSerializer, AnalyticsEventSerializer
)
from .stripe_utils import StripePaymentProcessor
from .services.webhook_service import StripeWebhookHandler


class PaymentIntentView(APIView):
    """Create Stripe PaymentIntent for subscription upgrades"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Create a payment intent"""
        try:
            tier_id = request.data.get('tier_id')
            billing_period = request.data.get('billing_period', 'monthly')
            
            if not tier_id:
                return Response(
                    {'error': 'tier_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            tier = Tier.objects.get(id=tier_id)
            
            # Create Stripe PaymentIntent
            intent_data = StripePaymentProcessor.create_payment_intent(
                request.user, tier, billing_period
            )
            
            return Response(intent_data, status=status.HTTP_200_OK)
        
        except Tier.DoesNotExist:
            return Response(
                {'error': 'Tier not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ConfirmPaymentView(APIView):
    """Confirm Stripe payment and upgrade subscription"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Confirm payment and create subscription"""
        try:
            payment_intent_id = request.data.get('payment_intent_id')
            tier_id = request.data.get('tier_id')
            billing_period = request.data.get('billing_period', 'monthly')
            
            if not payment_intent_id or not tier_id:
                return Response(
                    {'error': 'payment_intent_id and tier_id are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            tier = Tier.objects.get(id=tier_id)
            
            # Confirm payment with Stripe
            payment = StripePaymentProcessor.confirm_payment(
                payment_intent_id, tier, billing_period
            )
            
            # Generate PDF invoice after successful payment
            try:
                from api.services.invoice_service import InvoicePDFGenerator
                invoice = payment.invoice if hasattr(payment, 'invoice') and payment.invoice else Invoice.objects.filter(payment=payment).first()
                
                if invoice:
                    # Prepare invoice data for PDF generation
                    invoice_data = {
                        'invoice_id': invoice.invoice_number,
                        'invoice_date': invoice.created_at.strftime('%B %d, %Y'),
                        'due_date': invoice.due_date.strftime('%B %d, %Y'),
                        'user_name': request.user.get_full_name() or request.user.username,
                        'user_email': request.user.email,
                        'tier_name': tier.display_name if tier else 'Unknown',
                        'tier_description': tier.description if tier else '',
                        'billing_period': 'Monthly' if billing_period == 'monthly' else 'Yearly',
                        'amount': float(payment.amount),
                        'status': 'Paid',
                        'paid_date': datetime.now().strftime('%B %d, %Y'),
                    }
                    
                    pdf_result = InvoicePDFGenerator.generate_invoice_pdf(invoice_data)
                    if pdf_result['success']:
                        invoice.pdf_file.name = pdf_result['file_path']
                        invoice.save(update_fields=['pdf_file'])
            except Exception as pdf_error:
                # Log PDF generation error but don't fail the payment confirmation
                print(f'Warning: Could not generate PDF invoice: {str(pdf_error)}')
            
            return Response(
                {
                    'message': 'Payment confirmed and subscription upgraded',
                    'payment': PaymentSerializer(payment).data,
                    'subscription': {
                        'tier': tier.display_name,
                        'billing_period': billing_period,
                        'renewal_date': request.user.subscription.renewal_date
                    }
                },
                status=status.HTTP_200_OK
            )
        
        except Tier.DoesNotExist:
            return Response(
                {'error': 'Tier not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentHistoryView(APIView):
    """Get user's payment history"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retrieve user's payment history"""
        try:
            payments = Payment.objects.filter(user=request.user).order_by('-created_at')[:50]
            
            return Response({
                'payments': PaymentSerializer(payments, many=True).data,
                'count': len(payments)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InvoiceListView(APIView):
    """Get user's invoices"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retrieve user's invoices"""
        try:
            invoices = Invoice.objects.filter(user=request.user).order_by('-created_at')[:50]
            
            return Response({
                'invoices': InvoiceSerializer(invoices, many=True).data,
                'count': len(invoices)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InvoiceDetailView(APIView):
    """Get specific invoice"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, invoice_id):
        """Retrieve specific invoice"""
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=request.user)
            
            return Response(
                InvoiceSerializer(invoice).data,
                status=status.HTTP_200_OK
            )
        
        except Invoice.DoesNotExist:
            return Response(
                {'error': 'Invoice not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AnalyticsEventView(APIView):
    """Log and retrieve analytics events"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Log a new analytics event"""
        try:
            event_type = request.data.get('event_type')
            event_name = request.data.get('event_name')
            page = request.data.get('page', '')
            metadata = request.data.get('metadata', {})
            duration_seconds = request.data.get('duration_seconds')
            session_id = request.data.get('session_id', '')
            
            if not event_type or not event_name:
                return Response(
                    {'error': 'event_type and event_name are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            event = AnalyticsEvent.objects.create(
                user=request.user,
                event_type=event_type,
                event_name=event_name,
                page=page,
                metadata=metadata,
                duration_seconds=duration_seconds,
                session_id=session_id
            )
            
            return Response(
                AnalyticsEventSerializer(event).data,
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request):
        """Retrieve user's analytics events"""
        try:
            # Get optional filters
            event_type = request.query_params.get('event_type')
            days = int(request.query_params.get('days', 30))
            
            # Build query
            events = AnalyticsEvent.objects.filter(user=request.user)
            
            if event_type:
                events = events.filter(event_type=event_type)
            
            # Filter by date range
            since = datetime.now() - timedelta(days=days)
            events = events.filter(created_at__gte=since).order_by('-created_at')[:500]
            
            return Response({
                'events': AnalyticsEventSerializer(events, many=True).data,
                'count': len(events)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AnalyticsDashboardView(APIView):
    """Get analytics summary for user dashboard"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retrieve analytics summary"""
        try:
            days = int(request.query_params.get('days', 30))
            
            since = datetime.now() - timedelta(days=days)
            
            # Get user subscription info
            subscription = request.user.subscription
            
            # Get event counts by type
            events = AnalyticsEvent.objects.filter(
                user=request.user,
                created_at__gte=since
            )
            
            event_breakdown = {}
            for event_type, display in AnalyticsEvent.EVENT_TYPES:
                count = events.filter(event_type=event_type).count()
                event_breakdown[event_type] = count
            
            # Calculate engagement metrics
            total_events = events.count()
            unique_dates = events.values('created_at__date').distinct().count()
            
            # Get most visited pages
            top_pages = {}
            for event in events.filter(page__isnull=False):
                if event.page:
                    top_pages[event.page] = top_pages.get(event.page, 0) + 1
            
            top_pages_sorted = sorted(
                top_pages.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
            
            return Response({
                'period_days': days,
                'subscription': {
                    'tier': subscription.tier.display_name if subscription.tier else 'Free',
                    'tokens_remaining': subscription.tokens_remaining() if subscription.tier else 0,
                    'tokens_limit': subscription.tier.monthly_tokens if subscription.tier else 0,
                },
                'engagement': {
                    'total_events': total_events,
                    'active_days': unique_dates,
                    'avg_daily_events': round(total_events / max(unique_dates, 1), 2)
                },
                'event_breakdown': event_breakdown,
                'top_pages': [{'page': page, 'count': count} for page, count in top_pages_sorted]
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WebhookView(APIView):
    """Handle Stripe webhooks with signature validation and event processing"""
    permission_classes = [AllowAny]
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        """Process incoming Stripe webhook events"""
        try:
            payload = request.body
            sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
            
            # Validate signature
            if not sig_header:
                return Response(
                    {'error': 'Missing Stripe-Signature header'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Use webhook handler to validate and process event
            handler = StripeWebhookHandler()
            event = handler.validate_signature(payload, sig_header)
            
            if event is None:
                return Response(
                    {'error': 'Invalid webhook signature'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Process the event
            result = handler.process_event(event)
            
            # Return 200 to acknowledge receipt (required by Stripe)
            return Response(
                {
                    'received': True,
                    'event_id': event.get('id'),
                    'event_type': event.get('type'),
                    'result': result
                },
                status=status.HTTP_200_OK
            )
        
        except json.JSONDecodeError:
            return Response(
                {'error': 'Invalid JSON payload'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Webhook processing error: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TierUpgradeView(APIView):
    """Handle subscription tier upgrades/downgrades"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Process tier change request"""
        try:
            from api.services.email_service import EmailService
            
            to_tier_id = request.data.get('to_tier_id')
            billing_period = request.data.get('billing_period', 'monthly')
            
            if not to_tier_id:
                return Response(
                    {'error': 'to_tier_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            to_tier = Tier.objects.get(id=to_tier_id)
            
            # Get current subscription
            subscription = UserSubscription.objects.filter(user=request.user).first()
            from_tier = subscription.tier if subscription else None
            
            # Process tier upgrade with proration
            result = StripePaymentProcessor.process_tier_upgrade(
                request.user, from_tier, to_tier, billing_period
            )
            
            # Send confirmation email
            try:
                if result.get('amount_due', 0) > 0:
                    EmailService.send_payment_confirmation(
                        request.user,
                        to_tier,
                        result.get('amount_due', 0),
                        billing_period,
                        invoice_id=result.get('tier_change_id')
                    )
                else:
                    # Free tier or credit applied - send upgrade email
                    EmailService.send_subscription_upgrade_email(
                        request.user,
                        from_tier,
                        to_tier,
                        amount=result.get('amount_due', 0)
                    )
            except Exception as email_error:
                # Log email error but don't fail the upgrade
                print(f'Error sending upgrade email: {str(email_error)}')
            
            return Response(result, status=status.HTTP_200_OK)
        
        except Tier.DoesNotExist:
            return Response(
                {'error': 'Tier not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class GetAvailableTiersView(APIView):
    """Get all available subscription tiers"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Retrieve all available tiers"""
        try:
            tiers = Tier.objects.filter(is_active=True).order_by('price_monthly')
            
            from .serializers import TierSerializer
            serializer = TierSerializer(tiers, many=True)
            
            return Response({
                'tiers': serializer.data,
                'count': tiers.count()
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class GetCurrentTierView(APIView):
    """Get current user's tier and subscription details"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user's current tier info"""
        try:
            subscription = UserSubscription.objects.filter(user=request.user).first()
            
            if not subscription or not subscription.tier:
                return Response({
                    'tier': None,
                    'tier_name': 'Free',
                    'tokens_remaining': 0,
                    'tokens_limit': 0,
                    'expires_at': None
                }, status=status.HTTP_200_OK)
            
            from .serializers import UserSubscriptionSerializer
            serializer = UserSubscriptionSerializer(subscription)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class GenerateInvoicePDFView(APIView):
    """Generate PDF for an invoice"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, invoice_id):
        """Generate or regenerate PDF for invoice"""
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=request.user)
            
            from api.services.invoice_service import InvoicePDFGenerator
            
            # Prepare invoice data
            invoice_data = {
                'invoice_id': invoice.invoice_number,
                'invoice_date': invoice.created_at.strftime('%B %d, %Y'),
                'due_date': invoice.due_date.strftime('%B %d, %Y'),
                'user_name': request.user.get_full_name() or request.user.username,
                'user_email': request.user.email,
                'tier_name': invoice.tier.display_name if invoice.tier else 'Unknown',
                'tier_description': invoice.tier.description if invoice.tier else '',
                'billing_period': 'Monthly' if invoice.payment and invoice.payment.billing_period == 'monthly' else 'Yearly',
                'amount': float(invoice.amount),
                'status': invoice.get_status_display(),
            }
            
            # Generate PDF
            result = InvoicePDFGenerator.generate_invoice_pdf(invoice_data)
            
            if result['success']:
                # Update invoice with PDF file path
                from django.core.files.base import ContentFile
                invoice.pdf_file.name = result['file_path']
                invoice.save(update_fields=['pdf_file'])
                
                return Response({
                    'success': True,
                    'message': 'PDF generated successfully',
                    'file_path': result['file_path']
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': result.get('error', 'Failed to generate PDF')
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Invoice.DoesNotExist:
            return Response(
                {'error': 'Invoice not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class DownloadInvoicePDFView(APIView):
    """Download PDF invoice file"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, invoice_id):
        """Download invoice PDF"""
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=request.user)
            
            # Check if PDF exists
            if not invoice.pdf_file:
                return Response(
                    {'error': 'PDF not yet generated. Please generate it first.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Return file download response
            from django.http import FileResponse
            
            response = FileResponse(
                invoice.pdf_file.open('rb'),
                as_attachment=True,
                filename=f"Invoice_{invoice.invoice_number}.pdf"
            )
            response['Content-Type'] = 'application/pdf'
            
            return response
        
        except Invoice.DoesNotExist:
            return Response(
                {'error': 'Invoice not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ExportPaymentsView(APIView):
    """Export payment history as CSV or JSON"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Export payments in requested format"""
        try:
            from django.http import HttpResponse
            from api.services.export_service import DataExportService
            
            format_type = request.query_params.get('format', 'csv').lower()
            days = int(request.query_params.get('days', 30))
            
            if format_type not in ['csv', 'json']:
                return Response(
                    {'error': 'Invalid format. Use "csv" or "json"'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if format_type == 'csv':
                content = DataExportService.export_payments_csv(request.user, days)
                response = HttpResponse(content, content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="payments_{datetime.now().strftime("%Y%m%d")}.csv"'
            else:  # json
                content = DataExportService.export_payments_json(request.user, days)
                response = HttpResponse(content, content_type='application/json')
                response['Content-Disposition'] = f'attachment; filename="payments_{datetime.now().strftime("%Y%m%d")}.json"'
            
            return response
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExportInvoicesView(APIView):
    """Export invoices as CSV or JSON"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Export invoices in requested format"""
        try:
            from django.http import HttpResponse
            from api.services.export_service import DataExportService
            
            format_type = request.query_params.get('format', 'csv').lower()
            days = int(request.query_params.get('days', 30))
            
            if format_type not in ['csv', 'json']:
                return Response(
                    {'error': 'Invalid format. Use "csv" or "json"'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if format_type == 'csv':
                content = DataExportService.export_invoices_csv(request.user, days)
                response = HttpResponse(content, content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="invoices_{datetime.now().strftime("%Y%m%d")}.csv"'
            else:  # json
                content = DataExportService.export_invoices_json(request.user, days)
                response = HttpResponse(content, content_type='application/json')
                response['Content-Disposition'] = f'attachment; filename="invoices_{datetime.now().strftime("%Y%m%d")}.json"'
            
            return response
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExportAnalyticsView(APIView):
    """Export analytics events as CSV or JSON"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Export analytics in requested format"""
        try:
            from django.http import HttpResponse
            from api.services.export_service import DataExportService
            
            format_type = request.query_params.get('format', 'csv').lower()
            days = int(request.query_params.get('days', 30))
            event_type = request.query_params.get('event_type', None)
            
            if format_type not in ['csv', 'json']:
                return Response(
                    {'error': 'Invalid format. Use "csv" or "json"'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if format_type == 'csv':
                content = DataExportService.export_analytics_csv(request.user, days, event_type)
                response = HttpResponse(content, content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="analytics_{datetime.now().strftime("%Y%m%d")}.csv"'
            else:  # json
                content = DataExportService.export_analytics_json(request.user, days, event_type)
                response = HttpResponse(content, content_type='application/json')
                response['Content-Disposition'] = f'attachment; filename="analytics_{datetime.now().strftime("%Y%m%d")}.json"'
            
            # Log export event
            AnalyticsEvent.objects.create(
                user=request.user,
                event_type='export',
                event_name='Analytics Data Exported',
                metadata={'format': format_type, 'days': days, 'event_type': event_type},
                page='analytics'
            )
            
            return response
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExportUserDataView(APIView):
    """Export comprehensive user data as CSV or JSON"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Export user data in requested format"""
        try:
            from django.http import HttpResponse
            from api.services.export_service import DataExportService
            
            format_type = request.query_params.get('format', 'csv').lower()
            
            if format_type not in ['csv', 'json']:
                return Response(
                    {'error': 'Invalid format. Use "csv" or "json"'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if format_type == 'csv':
                content = DataExportService.export_user_data_csv(request.user)
                response = HttpResponse(content, content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="user_data_{datetime.now().strftime("%Y%m%d")}.csv"'
            else:  # json
                content = DataExportService.export_user_data_json(request.user)
                response = HttpResponse(content, content_type='application/json')
                response['Content-Disposition'] = f'attachment; filename="user_data_{datetime.now().strftime("%Y%m%d")}.json"'
            
            # Log export event
            AnalyticsEvent.objects.create(
                user=request.user,
                event_type='export',
                event_name='User Data Exported',
                metadata={'format': format_type},
                page='account'
            )
            
            return response
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WebhookEventListView(APIView):
    """List webhook events with filtering and pagination"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get webhook events"""
        try:
            # Get query parameters
            status_filter = request.query_params.get('status')
            event_type = request.query_params.get('event_type')
            limit = int(request.query_params.get('limit', 50))
            offset = int(request.query_params.get('offset', 0))
            
            # Start with all webhook events
            queryset = WebhookEvent.objects.all()
            
            # Filter by user if not admin
            if request.user.profile and request.user.profile.role != 'admin':
                queryset = queryset.filter(user=request.user)
            
            # Apply filters
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            if event_type:
                queryset = queryset.filter(event_type=event_type)
            
            # Order by received date
            queryset = queryset.order_by('-received_at')
            
            # Get total count
            total_count = queryset.count()
            
            # Paginate
            events = queryset[offset:offset + limit]
            
            # Serialize events
            events_data = []
            for event in events:
                events_data.append({
                    'id': event.id,
                    'stripe_event_id': event.stripe_event_id,
                    'event_type': event.event_type,
                    'status': event.status,
                    'error_message': event.error_message,
                    'retry_count': event.retry_count,
                    'received_at': event.received_at.isoformat(),
                    'processed_at': event.processed_at.isoformat() if event.processed_at else None,
                    'user_email': event.user.email if event.user else None,
                    'payment_id': event.payment.id if event.payment else None,
                })
            
            return Response({
                'count': total_count,
                'events': events_data,
                'limit': limit,
                'offset': offset
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WebhookEventDetailView(APIView):
    """Get details of a specific webhook event"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, event_id):
        """Get webhook event details"""
        try:
            event = WebhookEvent.objects.get(id=event_id)
            
            # Check permissions
            if request.user.profile and request.user.profile.role != 'admin':
                if event.user != request.user:
                    return Response(
                        {'error': 'Permission denied'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            event_data = {
                'id': event.id,
                'stripe_event_id': event.stripe_event_id,
                'event_type': event.event_type,
                'api_version': event.api_version,
                'status': event.status,
                'error_message': event.error_message,
                'retry_count': event.retry_count,
                'received_at': event.received_at.isoformat(),
                'processed_at': event.processed_at.isoformat() if event.processed_at else None,
                'updated_at': event.updated_at.isoformat(),
                'user_email': event.user.email if event.user else None,
                'payment_id': event.payment.id if event.payment else None,
                'raw_data': event.raw_data,
            }
            
            return Response(event_data, status=status.HTTP_200_OK)
        
        except WebhookEvent.DoesNotExist:
            return Response(
                {'error': 'Webhook event not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WebhookEventRetryView(APIView):
    """Retry processing a failed webhook event (admin only)"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, event_id):
        """Retry a failed webhook event"""
        try:
            # Check if user is admin
            if not request.user.profile or request.user.profile.role != 'admin':
                return Response(
                    {'error': 'Admin access required'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            event = WebhookEvent.objects.get(id=event_id)
            
            # Only retry failed or ignored events
            if event.status not in ['failed', 'ignored']:
                return Response(
                    {'error': f'Cannot retry event with status: {event.status}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Process the event
            from .services.webhook_service import StripeWebhookHandler, WebhookRetryManager
            result = WebhookRetryManager.retry_event(event)
            
            return Response({
                'message': 'Webhook event retry initiated',
                'event_id': event_id,
                'result': result
            }, status=status.HTTP_200_OK)
        
        except WebhookEvent.DoesNotExist:
            return Response(
                {'error': 'Webhook event not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WebhookStatsView(APIView):
    """Get webhook statistics and summary"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get webhook statistics"""
        try:
            # Check if user is admin
            if not request.user.profile or request.user.profile.role != 'admin':
                return Response(
                    {'error': 'Admin access required'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Get statistics
            total_events = WebhookEvent.objects.count()
            succeeded_events = WebhookEvent.objects.filter(status='succeeded').count()
            failed_events = WebhookEvent.objects.filter(status='failed').count()
            processing_events = WebhookEvent.objects.filter(status='processing').count()
            ignored_events = WebhookEvent.objects.filter(status='ignored').count()
            
            # Get event type breakdown
            from django.db.models import Count
            event_type_stats = WebhookEvent.objects.values('event_type').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Get recent failed events
            recent_failed = WebhookEvent.objects.filter(
                status='failed'
            ).order_by('-received_at')[:5].values(
                'id', 'stripe_event_id', 'event_type', 'error_message', 'received_at'
            )
            
            stats_data = {
                'total_events': total_events,
                'succeeded': succeeded_events,
                'failed': failed_events,
                'processing': processing_events,
                'ignored': ignored_events,
                'event_type_breakdown': list(event_type_stats),
                'recent_failed_events': list(recent_failed),
                'success_rate': round((succeeded_events / total_events * 100), 2) if total_events > 0 else 0,
            }
            
            return Response(stats_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
