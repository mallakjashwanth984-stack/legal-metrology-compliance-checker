from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
import os

class ReportGenerator:
    """
    Generate compliance reports in PDF format
    """
    
    def __init__(self):
        self.page_size = A4
        self.styles = getSampleStyleSheet()
        self._define_custom_styles()
    
    def _define_custom_styles(self):
        """
        Define custom paragraph styles
        """
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
    
    def generate_pdf_report(self, report, product, violations):
        """
        Generate a PDF compliance report
        """
        # Create report file path
        report_dir = 'uploads/reports'
        os.makedirs(report_dir, exist_ok=True)
        
        filename = f'compliance_report_{report.id}_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.pdf'
        filepath = os.path.join(report_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=self.page_size,
                              rightMargin=0.75*inch, leftMargin=0.75*inch,
                              topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        # Build story
        story = []
        
        # Title
        story.append(Paragraph('COMPLIANCE REPORT', self.styles['CustomTitle']))
        story.append(Paragraph('Legal Metrology (Packaged Commodities) Rules, 2011', self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Report Header
        story.append(Paragraph('REPORT INFORMATION', self.styles['CustomHeading']))
        header_data = [
            ['Report ID:', f'#{report.id}'],
            ['Generated Date:', datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')],
            ['Compliance Status:', self._get_status_with_color(report.compliance_status)],
        ]
        header_table = Table(header_data, colWidths=[2*inch, 3*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Product Information
        story.append(Paragraph('PRODUCT INFORMATION', self.styles['CustomHeading']))
        product_data = [
            ['Product Name:', product.product_name or 'N/A'],
            ['Category:', product.product_category or 'N/A'],
            ['Manufacturer:', product.manufacturer_name or 'N/A'],
            ['Barcode:', product.barcode or 'N/A'],
            ['Net Quantity:', f"{product.net_quantity} {product.unit_of_measurement}" if product.net_quantity else 'N/A'],
            ['MRP:', f'₹ {product.mrp}' if product.mrp else 'N/A'],
        ]
        product_table = Table(product_data, colWidths=[2*inch, 3*inch])
        product_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(product_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Compliance Summary
        story.append(Paragraph('COMPLIANCE SUMMARY', self.styles['CustomHeading']))
        summary_data = [
            ['Compliance Percentage:', f"{report.compliance_percentage:.1f}%"],
            ['Total Violations:', str(report.total_violations)],
            ['Critical Violations:', str(report.critical_violations)],
            ['Major Violations:', str(report.major_violations)],
            ['Minor Violations:', str(report.minor_violations)],
        ]
        summary_table = Table(summary_data, colWidths=[2*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff3cd') if report.compliance_status == 'non_compliant' else colors.HexColor('#d4edda')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Violations Details
        if violations:
            story.append(PageBreak())
            story.append(Paragraph('VIOLATIONS DETAILS', self.styles['CustomHeading']))
            
            # Sort violations by severity
            severity_order = {'critical': 0, 'major': 1, 'minor': 2}
            sorted_violations = sorted(violations, key=lambda x: severity_order.get(x.severity, 3))
            
            violations_data = [['Severity', 'Violation Type', 'Description', 'Rule Reference']]
            
            for violation in sorted_violations:
                violations_data.append([
                    self._get_severity_badge(violation.severity),
                    violation.violation_type.replace('_', ' ').title(),
                    violation.description,
                    violation.rule_reference or 'N/A'
                ])
            
            violations_table = Table(violations_data, colWidths=[1*inch, 1.5*inch, 2*inch, 1.5*inch])
            violations_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(violations_table)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            f'<i>Report generated on {datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")} by Legal Metrology Compliance Checker System</i>',
            self.styles['Normal']
        ))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _get_status_with_color(self, status):
        """
        Get status text with color coding
        """
        if status == 'compliant':
            return '<font color="green"><b>✓ COMPLIANT</b></font>'
        else:
            return '<font color="red"><b>✗ NON-COMPLIANT</b></font>'
    
    def _get_severity_badge(self, severity):
        """
        Get severity badge with appropriate styling
        """
        colors_map = {
            'critical': 'red',
            'major': 'orange',
            'minor': 'yellow'
        }
        color = colors_map.get(severity, 'gray')
        return f'<font color="{color}"><b>{severity.upper()}</b></font>'
