from app import db
from datetime import datetime

class Violation(db.Model):
    __tablename__ = 'violations'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    violation_type = db.Column(db.String(120), nullable=False)  # e.g., missing_declaration, incorrect_font_size, etc.
    severity = db.Column(db.String(20))  # critical, major, minor
    description = db.Column(db.Text)
    rule_reference = db.Column(db.String(255))  # Reference to Legal Metrology Rules
    is_resolved = db.Column(db.Boolean, default=False)
    resolution_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'violation_type': self.violation_type,
            'severity': self.severity,
            'description': self.description,
            'rule_reference': self.rule_reference,
            'is_resolved': self.is_resolved,
            'created_at': self.created_at.isoformat()
        }
