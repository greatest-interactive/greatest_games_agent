"""
Invoice PDF Generation Service
Handles creation and storage of invoice PDFs using reportlab
"""

import os
from io import BytesIO
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, grey, white
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT


class InvoicePDFGenerator:
    """
    Service for generating PDF invoices using reportlab
    """
    
    # PDF configuration
    PAGE_SIZE = letter
    MARGIN = 0.5 * inch
    WIDTH = PAGE_SIZE[0] - (2 * MARGIN)
    
    # Colors
    PRIMARY_COLOR = HexColor('#2563eb')
    HEADER_COLOR = HexColor('#1e3a8a')
    FOOTER_COLOR = HexColor('#f3f4f6')
    TEXT_COLOR = HexColor('#1f2937')
    
    @staticmethod
    def get_styles():
        """Get or create custom paragraph styles"""
        styles = getSampleStyleSheet()
        
        # Company header style
        styles.add(ParagraphStyle(
            name='CompanyName',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=InvoicePDFGenerator.HEADER_COLOR,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        # Invoice title style
        styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=InvoicePDFGenerator.PRIMARY_COLOR,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading3'],
            fontSize=11,
            textColor=InvoicePDFGenerator.HEADER_COLOR,
            spaceAfter=8,
            fontName='Helvetica-Bold',
            borderPadding=6
        ))
        
        # Normal text style
        styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=InvoicePDFGenerator.TEXT_COLOR,
            spaceAfter=6
        ))
        
        # Small text style for footer
        styles.add(ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=grey,
            spaceAfter=4
        ))
        
        return styles
    
    @staticmethod
    def _ensure_media_directory():
        """Ensure the invoices directory exists"""
        invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
        os.makedirs(invoice_dir, exist_ok=True)
        return invoice_dir
    
    @classmethod
    def generate_invoice_pdf(cls, invoice_data, output_path=None):
        """
        Generate a PDF invoice from invoice data
        
        Args:
            invoice_data (dict): Invoice data including:
                - invoice_id: Invoice number/ID
                - invoice_date: Date invoice was created
                - due_date: Payment due date
                - user_name: Customer name
                - user_email: Customer email
                - tier_name: Subscription tier name
                - tier_description: Tier description
                - billing_period: Monthly/Yearly
                - amount: Amount charged
                - status: Invoice status (Paid/Pending/Failed)
                - company_name: Company name (optional)
                - company_address: Company address (optional)
                - company_email: Company email (optional)
            
            output_path (str): Optional path to save PDF. If not provided, 
                              uses default media path
        
        Returns:
            dict: {
                'success': bool,
                'file_path': str (relative path for storage),
                'full_path': str (absolute path for download),
                'error': str (if failed)
            }
        """
        try:
            styles = cls.get_styles()
            
            # Create or use provided output path
            if not output_path:
                invoice_dir = cls._ensure_media_directory()
                filename = f"invoice_{invoice_data.get('invoice_id', 'unknown')}.pdf"
                output_path = os.path.join(invoice_dir, filename)
            
            # Create PDF document
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=cls.PAGE_SIZE,
                rightMargin=cls.MARGIN,
                leftMargin=cls.MARGIN,
                topMargin=cls.MARGIN,
                bottomMargin=cls.MARGIN,
                title=f"Invoice #{invoice_data.get('invoice_id', 'unknown')}"
            )
            
            # Build document elements
            elements = []
            
            # Header section
            company_name = invoice_data.get('company_name', 'Greatest Game Agent')
            elements.append(Paragraph(company_name, styles['CompanyName']))
            
            company_email = invoice_data.get('company_email', 'support@greatestgame.com')
            company_address = invoice_data.get('company_address', 'Games Analytics Platform')
            elements.append(Paragraph(f"{company_address}", styles['CustomNormal']))
            elements.append(Paragraph(f"<font color='#666'>{company_email}</font>", styles['Footer']))
            elements.append(Spacer(1, 0.2 * inch))
            
            # Invoice title and number
            elements.append(Paragraph("INVOICE", styles['InvoiceTitle']))
            
            # Invoice details table
            invoice_details = [
                ['Invoice Number:', f"#{invoice_data.get('invoice_id', 'N/A')}"],
                ['Invoice Date:', invoice_data.get('invoice_date', 'N/A')],
                ['Due Date:', invoice_data.get('due_date', 'N/A')],
                ['Status:', invoice_data.get('status', 'Pending')],
            ]
            
            invoice_table = Table(invoice_details, colWidths=[cls.WIDTH * 0.4, cls.WIDTH * 0.6])
            invoice_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
                ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#374151')),
                ('TEXTCOLOR', (1, 0), (1, -1), cls.TEXT_COLOR),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [white, HexColor('#f9fafb')]),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(invoice_table)
            elements.append(Spacer(1, 0.3 * inch))
            
            # Bill To section
            elements.append(Paragraph("BILL TO", styles['SectionHeader']))
            bill_to_data = [
                ['Customer:', invoice_data.get('user_name', 'Customer')],
                ['Email:', invoice_data.get('user_email', 'customer@example.com')],
            ]
            bill_table = Table(bill_to_data, colWidths=[cls.WIDTH * 0.25, cls.WIDTH * 0.75])
            bill_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
                ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#374151')),
                ('TEXTCOLOR', (1, 0), (1, -1), cls.TEXT_COLOR),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(bill_table)
            elements.append(Spacer(1, 0.3 * inch))
            
            # Items table
            elements.append(Paragraph("INVOICE DETAILS", styles['SectionHeader']))
            
            items_data = [
                ['Description', 'Billing Period', 'Amount'],
                [
                    invoice_data.get('tier_name', 'Subscription'),
                    invoice_data.get('billing_period', 'Monthly').capitalize(),
                    f"${Decimal(str(invoice_data.get('amount', 0))):.2f}"
                ]
            ]
            
            items_table = Table(items_data, colWidths=[cls.WIDTH * 0.5, cls.WIDTH * 0.25, cls.WIDTH * 0.25])
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), cls.PRIMARY_COLOR),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('FONT', (0, 1), (-1, -1), 'Helvetica', 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f9fafb')]),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb')),
            ]))
            elements.append(items_table)
            elements.append(Spacer(1, 0.2 * inch))
            
            # Totals section
            totals_data = [
                ['', 'Subtotal:', f"${Decimal(str(invoice_data.get('amount', 0))):.2f}"],
                ['', 'Tax:', '$0.00'],
                ['', 'Total:', f"${Decimal(str(invoice_data.get('amount', 0))):.2f}"],
            ]
            
            totals_table = Table(totals_data, colWidths=[cls.WIDTH * 0.5, cls.WIDTH * 0.25, cls.WIDTH * 0.25])
            totals_table.setStyle(TableStyle([
                ('ALIGN', (1, 0), (2, -1), 'RIGHT'),
                ('FONT', (0, 0), (-1, -2), 'Helvetica', 9),
                ('FONT', (1, -1), (2, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (1, -1), (2, -1), 11),
                ('TEXTCOLOR', (1, -1), (2, -1), cls.PRIMARY_COLOR),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LINEABOVE', (1, -1), (2, -1), 2, cls.PRIMARY_COLOR),
            ]))
            elements.append(totals_table)
            elements.append(Spacer(1, 0.4 * inch))
            
            # Notes section
            status = invoice_data.get('status', 'Pending')
            if status == 'Paid':
                note_text = f"<b>Thank you for your payment!</b><br/>This invoice has been paid in full on {invoice_data.get('paid_date', 'the payment date')}."
                note_color = '#166534'
                note_bg = '#f0fdf4'
            elif status == 'Pending':
                note_text = "<b>Payment Due:</b><br/>Please remit payment according to the terms shown above."
                note_color = '#92400e'
                note_bg = '#fef3c7'
            else:
                note_text = "<b>Payment Status:</b><br/>Please contact support if you have any questions about this invoice."
                note_color = '#991b1b'
                note_bg = '#fee2e2'
            
            elements.append(Paragraph("NOTES", styles['SectionHeader']))
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(Paragraph(note_text, styles['CustomNormal']))
            
            elements.append(Spacer(1, 0.4 * inch))
            
            # Footer
            footer_text = (
                f"<font size='8' color='#666'>"
                f"This is an automated invoice generated by Greatest Game Agent.<br/>"
                f"For questions about this invoice, please contact support@greatestgame.com<br/>"
                f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
                f"</font>"
            )
            elements.append(Paragraph(footer_text, styles['Footer']))
            
            # Build PDF
            doc.build(elements)
            
            # Write to file
            pdf_buffer.seek(0)
            with open(output_path, 'wb') as pdf_file:
                pdf_file.write(pdf_buffer.getvalue())
            
            # Return relative path for storage
            relative_path = os.path.relpath(output_path, settings.MEDIA_ROOT)
            
            return {
                'success': True,
                'file_path': relative_path,
                'full_path': output_path,
                'file_size': os.path.getsize(output_path)
            }
        
        except Exception as e:
            return {
                'success': False,
                'file_path': None,
                'full_path': None,
                'error': str(e)
            }
    
    @classmethod
    def generate_invoice_for_payment(cls, payment_obj):
        """
        Generate PDF invoice for a Payment object
        
        Args:
            payment_obj: Payment model instance
        
        Returns:
            dict: Generation result with success status and file path
        """
        try:
            invoice_data = {
                'invoice_id': payment_obj.invoice.invoice_number if payment_obj.invoice else payment_obj.id,
                'invoice_date': payment_obj.created_at.strftime('%B %d, %Y'),
                'due_date': payment_obj.due_date.strftime('%B %d, %Y') if payment_obj.due_date else 'Upon Receipt',
                'user_name': payment_obj.user.get_full_name() or payment_obj.user.username,
                'user_email': payment_obj.user.email,
                'tier_name': payment_obj.tier.name if payment_obj.tier else 'Unknown',
                'tier_description': payment_obj.tier.description if payment_obj.tier else '',
                'billing_period': 'Monthly' if payment_obj.billing_period == 'monthly' else 'Yearly',
                'amount': float(payment_obj.amount),
                'status': 'Paid' if payment_obj.status == 'completed' else 'Pending' if payment_obj.status == 'pending' else 'Failed',
                'paid_date': payment_obj.updated_at.strftime('%B %d, %Y') if payment_obj.status == 'completed' else None,
            }
            
            return cls.generate_invoice_pdf(invoice_data)
        
        except Exception as e:
            return {
                'success': False,
                'file_path': None,
                'full_path': None,
                'error': f'Error generating invoice for payment {payment_obj.id}: {str(e)}'
            }
