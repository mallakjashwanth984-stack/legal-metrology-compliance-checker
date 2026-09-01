from app import db
from datetime import datetime

class ComplianceReport(db.Model):
    __tablename__ = 'compliance_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    report_title = db.Column(db.String(255))
    total_violations = db.Column(db.Integer, default=0)
    critical_violations = db.Column(db.Integer, default=0)
    major_violations = db.Column(db.Integer, default=0)
    minor_violations = db.Column(db.Integer, default=0)
    compliance_status = db.Column(db.String(20))  # compliant, non_compliant
    compliance_percentage = db.Column(db.Float)  # 0-100
    summary = db.Column(db.Text)
    detailed_findings = db.Column(db.JSON)
    report_file_path = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'report_title': self.report_title,
            'total_violations': self.total_violations,
            'critical_violations': self.critical_violations,
            'major_violations': self.major_violations,
            'minor_violations': self.minor_violations,
            'compliance_status': self.compliance_status,
            'compliance_percentage': self.compliance_percentage,
            'summary': self.summary,
            'created_at': self.created_at.isoformat()
        }
