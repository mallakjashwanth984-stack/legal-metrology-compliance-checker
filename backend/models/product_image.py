from app import db
from datetime import datetime
from enum import Enum

class ImageType(Enum):
    FRONT = 'front'
    BACK = 'back'
    SIDE = 'side'
    TOP = 'top'
    BOTTOM = 'bottom'

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_type = db.Column(db.Enum(ImageType), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    extracted_text = db.Column(db.Text)
    image_quality_score = db.Column(db.Float)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref=db.backref('images', lazy=True, cascade='all, delete-orphan'))
    uploaded_by_user = db.relationship('User', backref=db.backref('uploaded_images', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'image_type': self.image_type.value,
            'image_path': self.image_path,
            'extracted_text': self.extracted_text,
            'image_quality_score': self.image_quality_score,
            'uploaded_by': self.uploaded_by,
            'uploaded_by_name': self.uploaded_by_user.full_name or self.uploaded_by_user.username,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
