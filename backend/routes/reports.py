from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.compliance_report import ComplianceReport
from models.product import Product
from models.violation import Violation
from services.report_generator import ReportGenerator
import os

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/<int:product_id>', methods=['POST'])
@jwt_required()
def generate_report(product_id):
    user_id = get_jwt_identity()
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    violations = Violation.query.filter_by(product_id=product_id).all()
    
    critical = len([v for v in violations if v.severity == 'critical'])
    major = len([v for v in violations if v.severity == 'major'])
    minor = len([v for v in violations if v.severity == 'minor'])
    total = len(violations)
    
    # Calculate compliance percentage
    max_violations = 100  # Assuming max 100 violations for 0% compliance
    compliance_percentage = max(0, 100 - (total / max_violations * 100))
    
    compliance_status = 'compliant' if total == 0 else 'non_compliant'
    
    # Create compliance report
    report = ComplianceReport(
        product_id=product_id,
        report_title=f'Compliance Report - {product.product_name}',
        total_violations=total,
        critical_violations=critical,
        major_violations=major,
        minor_violations=minor,
        compliance_status=compliance_status,
        compliance_percentage=compliance_percentage,
        summary=f'This product has {total} violations',
        detailed_findings={
            'violations': [v.to_dict() for v in violations]
        },
        created_by=user_id
    )
    
    db.session.add(report)
    db.session.commit()
    
    # Generate PDF report
    report_generator = ReportGenerator()
    pdf_path = report_generator.generate_pdf_report(report, product, violations)
    
    report.report_file_path = pdf_path
    db.session.commit()
    
    return jsonify({
        'message': 'Report generated successfully',
        'report': report.to_dict(),
        'download_url': f'/api/reports/download/{report.id}'
    }), 201

@reports_bp.route('/', methods=['GET'])
@jwt_required()
def get_reports():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    product_id = request.args.get('product_id')
    
    query = ComplianceReport.query
    
    if product_id:
        query = query.filter_by(product_id=product_id)
    
    reports = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': reports.total,
        'pages': reports.pages,
        'current_page': page,
        'reports': [report.to_dict() for report in reports.items]
    }), 200

@reports_bp.route('/<int:report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    report = ComplianceReport.query.get(report_id)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    return jsonify(report.to_dict()), 200

@reports_bp.route('/download/<int:report_id>', methods=['GET'])
@jwt_required()
def download_report(report_id):
    report = ComplianceReport.query.get(report_id)
    
    if not report or not report.report_file_path:
        return jsonify({'error': 'Report not found'}), 404
    
    if not os.path.exists(report.report_file_path):
        return jsonify({'error': 'Report file not found'}), 404
    
    return send_file(report.report_file_path, as_attachment=True)
