from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    product_category = db.Column(db.String(120))
    manufacturer_name = db.Column(db.String(255))
    manufacturer_address = db.Column(db.Text)
    barcode = db.Column(db.String(50), unique=True, sparse=True)
    batch_number = db.Column(db.String(100))
    net_quantity = db.Column(db.String(100))
    unit_of_measurement = db.Column(db.String(50))
    mrp = db.Column(db.Float)
    manufacturing_date = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    image_path = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    declarations = db.relationship('Declaration', backref='product', lazy=True, cascade='all, delete-orphan')
    violations = db.relationship('Violation', backref='product', lazy=True, cascade='all, delete-orphan')
    compliance_reports = db.relationship('ComplianceReport', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'product_category': self.product_category,
            'manufacturer_name': self.manufacturer_name,
            'barcode': self.barcode,
            'batch_number': self.batch_number,
            'net_quantity': self.net_quantity,
            'unit_of_measurement': self.unit_of_measurement,
            'mrp': self.mrp,
            'manufacturing_date': self.manufacturing_date.isoformat() if self.manufacturing_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'image_path': self.image_path,
            'created_at': self.created_at.isoformat()
        }
