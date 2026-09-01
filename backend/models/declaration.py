from app import db
from datetime import datetime

class Declaration(db.Model):
    __tablename__ = 'declarations'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    declaration_type = db.Column(db.String(120), nullable=False)  # e.g., manufacturer_name, net_quantity, mrp, etc.
    extracted_text = db.Column(db.Text)
    font_size = db.Column(db.Float)
    position = db.Column(db.JSON)  # {x, y, width, height}
    is_readable = db.Column(db.Boolean, default=True)
    confidence_score = db.Column(db.Float)  # OCR confidence
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'declaration_type': self.declaration_type,
            'extracted_text': self.extracted_text,
            'font_size': self.font_size,
            'position': self.position,
            'is_readable': self.is_readable,
            'confidence_score': self.confidence_score
        }
