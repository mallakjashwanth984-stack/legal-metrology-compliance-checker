from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.product import Product
from models.compliance_report import ComplianceReport
from models.violation import Violation
from models.user import User
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/overview', methods=['GET'])
@jwt_required()
def get_overview():
    total_products = Product.query.count()
    total_reports = ComplianceReport.query.count()
    total_violations = Violation.query.count()
    
    compliant_products = ComplianceReport.query.filter_by(compliance_status='compliant').count()
    non_compliant_products = ComplianceReport.query.filter_by(compliance_status='non_compliant').count()
    
    critical_violations = Violation.query.filter_by(severity='critical').count()
    major_violations = Violation.query.filter_by(severity='major').count()
    minor_violations = Violation.query.filter_by(severity='minor').count()
    
    return jsonify({
        'total_products': total_products,
        'total_reports': total_reports,
        'total_violations': total_violations,
        'compliant_products': compliant_products,
        'non_compliant_products': non_compliant_products,
        'critical_violations': critical_violations,
        'major_violations': major_violations,
        'minor_violations': minor_violations,
        'average_compliance': round((compliant_products / max(total_reports, 1)) * 100, 2) if total_reports > 0 else 0
    }), 200

@dashboard_bp.route('/recent-inspections', methods=['GET'])
@jwt_required()
def get_recent_inspections():
    limit = request.args.get('limit', 10, type=int)
    
    products = Product.query.order_by(Product.created_at.desc()).limit(limit).all()
    
    inspections = []
    for product in products:
        report = ComplianceReport.query.filter_by(product_id=product.id).first()
        inspections.append({
            'product_id': product.id,
            'product_name': product.product_name,
            'inspection_date': product.created_at.isoformat(),
            'compliance_status': report.compliance_status if report else 'pending',
            'compliance_percentage': report.compliance_percentage if report else 0
        })
    
    return jsonify({'recent_inspections': inspections}), 200

@dashboard_bp.route('/violations-by-type', methods=['GET'])
@jwt_required()
def get_violations_by_type():
    violations_by_type = db.session.query(
        Violation.violation_type,
        func.count(Violation.id)
    ).group_by(Violation.violation_type).all()
    
    return jsonify({
        'violations_by_type': [
            {'type': vtype, 'count': count}
            for vtype, count in violations_by_type
        ]
    }), 200

@dashboard_bp.route('/compliance-trends', methods=['GET'])
@jwt_required()
def get_compliance_trends():
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    daily_data = db.session.query(
        func.date(ComplianceReport.created_at).label('date'),
        func.count(ComplianceReport.id).label('total_reports'),
        func.avg(ComplianceReport.compliance_percentage).label('avg_compliance')
    ).filter(ComplianceReport.created_at >= start_date).group_by(
        func.date(ComplianceReport.created_at)
    ).all()
    
    return jsonify({
        'compliance_trends': [
            {
                'date': str(date),
                'total_reports': total,
                'avg_compliance': round(avg, 2) if avg else 0
            }
            for date, total, avg in daily_data
        ]
    }), 200

@dashboard_bp.route('/top-violations', methods=['GET'])
@jwt_required()
def get_top_violations():
    limit = request.args.get('limit', 10, type=int)
    
    top_violations = db.session.query(
        Violation.violation_type,
        func.count(Violation.id).label('count')
    ).group_by(Violation.violation_type).order_by(
        func.count(Violation.id).desc()
    ).limit(limit).all()
    
    return jsonify({
        'top_violations': [
            {'type': vtype, 'count': count}
            for vtype, count in top_violations
        ]
    }), 200
