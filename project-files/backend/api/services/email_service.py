"""
Email service for sending payment confirmations, invoices, and subscription updates
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime


class EmailService:
    """Service for handling all email communications"""
    
    @staticmethod
    def send_payment_confirmation(user, tier, amount, billing_period, invoice_id=None):
        """
        Send payment confirmation email after successful upgrade
        
        Args:
            user: User object
            tier: Tier object with plan details
            amount: Payment amount (Decimal)
            billing_period: 'monthly' or 'yearly'
            invoice_id: Optional invoice ID for reference
        """
        subject = f'Payment Confirmation - Upgraded to {tier.display_name}'
        
        context = {
            'user_name': user.first_name or user.username,
            'tier_name': tier.display_name,
            'tier_description': tier.description,
            'amount': float(amount),
            'billing_period': 'Monthly' if billing_period == 'monthly' else 'Yearly',
            'invoice_id': invoice_id or 'N/A',
            'date': datetime.now().strftime('%B %d, %Y'),
            'renewal_date': (datetime.now() + __import__('datetime').timedelta(days=30 if billing_period == 'monthly' else 365)).strftime('%B %d, %Y'),
            'support_email': 'support@greatestgame.com',
        }
        
        return EmailService._send_templated_email(
            subject=subject,
            recipient_list=[user.email],
            template_name='payment_confirmation',
            context=context,
            user_email=user.email
        )
    
    @staticmethod
    def send_invoice_email(user, invoice, attachment_path=None):
        """
        Send invoice email with optional PDF attachment
        
        Args:
            user: User object
            invoice: Invoice object with billing details
            attachment_path: Optional path to PDF invoice file
        """
        subject = f'Invoice #{invoice.id} - {invoice.tier.display_name} Plan'
        
        context = {
            'user_name': user.first_name or user.username,
            'invoice_id': invoice.id,
            'tier_name': invoice.tier.display_name,
            'amount': float(invoice.amount),
            'billing_period': invoice.billing_period,
            'date': invoice.billing_date.strftime('%B %d, %Y') if invoice.billing_date else 'N/A',
            'due_date': invoice.due_date.strftime('%B %d, %Y') if invoice.due_date else 'N/A',
            'status': invoice.status.title(),
            'support_email': 'support@greatestgame.com',
        }
        
        return EmailService._send_templated_email(
            subject=subject,
            recipient_list=[user.email],
            template_name='invoice',
            context=context,
            user_email=user.email,
            attachment_path=attachment_path,
            attachment_name=f'invoice_{invoice.id}.pdf'
        )
    
    @staticmethod
    def send_subscription_upgrade_email(user, from_tier, to_tier, amount=None):
        """
        Send subscription upgrade notification email
        
        Args:
            user: User object
            from_tier: Previous Tier object
            to_tier: New Tier object
            amount: Amount charged (optional, may be 0 or credited)
        """
        from_tier_name = from_tier.display_name if from_tier else 'Free'
        subject = f'Subscription Upgraded - Welcome to {to_tier.display_name}!'
        
        context = {
            'user_name': user.first_name or user.username,
            'from_tier': from_tier_name,
            'to_tier': to_tier.display_name,
            'new_features': to_tier.features[:5],  # List first 5 features
            'amount': float(amount) if amount else 0,
            'date': datetime.now().strftime('%B %d, %Y'),
            'account_url': f'{settings.FRONTEND_URL}/account',
            'support_email': 'support@greatestgame.com',
        }
        
        return EmailService._send_templated_email(
            subject=subject,
            recipient_list=[user.email],
            template_name='subscription_upgrade',
            context=context,
            user_email=user.email
        )
    
    @staticmethod
    def send_subscription_downgrade_email(user, from_tier, to_tier):
        """
        Send subscription downgrade notification email
        
        Args:
            user: User object
            from_tier: Previous Tier object
            to_tier: New Tier object
        """
        to_tier_name = to_tier.display_name if to_tier else 'Free'
        subject = f'Subscription Downgraded to {to_tier_name}'
        
        context = {
            'user_name': user.first_name or user.username,
            'from_tier': from_tier.display_name,
            'to_tier': to_tier_name,
            'features_retained': to_tier.features[:5] if to_tier else [],
            'date': datetime.now().strftime('%B %d, %Y'),
            'upgrade_url': f'{settings.FRONTEND_URL}/plans',
            'support_email': 'support@greatestgame.com',
        }
        
        return EmailService._send_templated_email(
            subject=subject,
            recipient_list=[user.email],
            template_name='subscription_downgrade',
            context=context,
            user_email=user.email
        )
    
    @staticmethod
    def send_renewal_reminder_email(user, tier, renewal_date):
        """
        Send subscription renewal reminder email
        
        Args:
            user: User object
            tier: Current Tier object
            renewal_date: Date of next renewal
        """
        subject = f'Your {tier.display_name} subscription renews soon'
        
        context = {
            'user_name': user.first_name or user.username,
            'tier_name': tier.display_name,
            'renewal_date': renewal_date.strftime('%B %d, %Y') if renewal_date else 'N/A',
            'account_url': f'{settings.FRONTEND_URL}/account',
            'support_email': 'support@greatestgame.com',
        }
        
        return EmailService._send_templated_email(
            subject=subject,
            recipient_list=[user.email],
            template_name='renewal_reminder',
            context=context,
            user_email=user.email
        )
    
    @staticmethod
    def send_failed_payment_email(user, tier, error_message=''):
        """
        Send failed payment notification email
        
        Args:
            user: User object
            tier: Tier that failed payment
            error_message: Error details from payment processor
        """
        subject = f'Payment Failed - Action Required for {tier.display_name}'
        
        context = {
            'user_name': user.first_name or user.username,
            'tier_name': tier.display_name,
            'error_message': error_message or 'Your card was declined. Please try again.',
            'date': datetime.now().strftime('%B %d, %Y'),
            'billing_url': f'{settings.FRONTEND_URL}/billing',
            'support_email': 'support@greatestgame.com',
        }
        
        return EmailService._send_templated_email(
            subject=subject,
            recipient_list=[user.email],
            template_name='payment_failed',
            context=context,
            user_email=user.email
        )
    
    @staticmethod
    def _send_templated_email(subject, recipient_list, template_name, context, user_email=None, 
                            attachment_path=None, attachment_name=None):
        """
        Send a templated email (HTML + plain text)
        
        Args:
            subject: Email subject
            recipient_list: List of recipient emails
            template_name: Template name (without .html)
            context: Context dict for template rendering
            user_email: User's email for logging
            attachment_path: Optional path to file attachment
            attachment_name: Optional name for attachment
        
        Returns:
            Number of emails sent (1 if successful, 0 if failed)
        """
        try:
            # Try to render HTML template, fall back to plain text if not found
            try:
                html_content = render_to_string(f'emails/{template_name}.html', context)
            except Exception:
                html_content = None
            
            # Create plain text version
            plain_text = render_to_string(f'emails/{template_name}.txt', context) if html_content else f'{subject}\n\n{str(context)}'
            
            # Create email
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipient_list
            )
            
            # Attach HTML version if available
            if html_content:
                email.attach_alternative(html_content, 'text/html')
            
            # Attach file if provided
            if attachment_path and attachment_name:
                try:
                    with open(attachment_path, 'rb') as attachment:
                        email.attach(attachment_name, attachment.read(), 'application/pdf')
                except Exception as e:
                    print(f'Failed to attach file: {str(e)}')
            
            # Send email
            result = email.send()
            
            return result
        
        except Exception as e:
            print(f'Error sending email to {user_email}: {str(e)}')
            return 0
    
    @staticmethod
    def send_bulk_email(subject, recipient_list, html_content, plain_text=None):
        """
        Send bulk email to multiple recipients
        
        Args:
            subject: Email subject
            recipient_list: List of recipient emails
            html_content: HTML email body
            plain_text: Plain text alternative
        
        Returns:
            Number of emails sent
        """
        try:
            if not plain_text:
                plain_text = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipient_list
            )
            
            email.attach_alternative(html_content, 'text/html')
            
            return email.send()
        
        except Exception as e:
            print(f'Error sending bulk email: {str(e)}')
            return 0
