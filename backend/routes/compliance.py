from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.product import Product
from models.compliance_report import ComplianceReport
from models.violation import Violation
from models.declaration import Declaration
from services.compliance_checker import ComplianceChecker
import os

compliance_bp = Blueprint('compliance', __name__)

@compliance_bp.route('/check/<int:product_id>', methods=['POST'])
@jwt_required()
def check_compliance(product_id):
    user_id = get_jwt_identity()
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Initialize compliance checker
    compliance_checker = ComplianceChecker()
    
    # Get all declarations for the product
    declarations = Declaration.query.filter_by(product_id=product_id).all()
    
    # Check compliance
    violations, compliance_status, compliance_percentage = compliance_checker.check_product_compliance(product, declarations)
    
    # Clear existing violations for this product
    Violation.query.filter_by(product_id=product_id).delete()
    
    # Store new violations
    critical_count = 0
    major_count = 0
    minor_count = 0
    
    for violation_data in violations:
        violation = Violation(
            product_id=product_id,
            violation_type=violation_data.get('type'),
            severity=violation_data.get('severity'),
            description=violation_data.get('description'),
            rule_reference=violation_data.get('rule_reference')
        )
        db.session.add(violation)
        
        if violation_data.get('severity') == 'critical':
            critical_count += 1
        elif violation_data.get('severity') == 'major':
            major_count += 1
        elif violation_data.get('severity') == 'minor':
            minor_count += 1
    
    db.session.commit()
    
    return jsonify({
        'product_id': product_id,
        'compliance_status': compliance_status,
        'compliance_percentage': compliance_percentage,
        'total_violations': len(violations),
        'critical_violations': critical_count,
        'major_violations': major_count,
        'minor_violations': minor_count,
        'violations': violations
    }), 200

@compliance_bp.route('/violations/<int:product_id>', methods=['GET'])
@jwt_required()
def get_violations(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    severity_filter = request.args.get('severity')
    
    query = Violation.query.filter_by(product_id=product_id)
    
    if severity_filter:
        query = query.filter_by(severity=severity_filter)
    
    violations = query.all()
    
    return jsonify({
        'product_id': product_id,
        'violations': [v.to_dict() for v in violations]
    }), 200

@compliance_bp.route('/violations/<int:violation_id>/resolve', methods=['PUT'])
@jwt_required()
def resolve_violation(violation_id):
    violation = Violation.query.get(violation_id)
    
    if not violation:
        return jsonify({'error': 'Violation not found'}), 404
    
    data = request.get_json()
    violation.is_resolved = True
    violation.resolution_notes = data.get('resolution_notes')
    from datetime import datetime
    violation.resolved_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Violation marked as resolved',
        'violation': violation.to_dict()
    }), 200
