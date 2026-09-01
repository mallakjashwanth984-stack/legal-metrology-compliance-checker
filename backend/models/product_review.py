from app import db
from datetime import datetime
from enum import Enum

class ReviewRating(Enum):
    ONE_STAR = 1
    TWO_STAR = 2
    THREE_STAR = 3
    FOUR_STAR = 4
    FIVE_STAR = 5

class ProductReview(db.Model):
    __tablename__ = 'product_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Enum(ReviewRating), nullable=False)
    title = db.Column(db.String(255))
    review_text = db.Column(db.Text)
    compliance_feedback = db.Column(db.String(50))  # 'compliant', 'non_compliant', 'needs_improvement'
    issues_found = db.Column(db.JSON)  # Store array of issues
    recommendations = db.Column(db.Text)  # Recommendations for improvement
    department = db.Column(db.String(100))  # Department of reviewer
    is_verified = db.Column(db.Boolean, default=False)  # Verified purchase/inspection
    helpful_count = db.Column(db.Integer, default=0)  # Upvotes
    unhelpful_count = db.Column(db.Integer, default=0)  # Downvotes
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref=db.backref('reviews', lazy=True, cascade='all, delete-orphan'))
    reviewer = db.relationship('User', backref=db.backref('reviews', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'reviewer_name': self.reviewer.full_name or self.reviewer.username,
            'reviewer_department': self.reviewer.department,
            'rating': self.rating.value,
            'title': self.title,
            'review_text': self.review_text,
            'compliance_feedback': self.compliance_feedback,
            'issues_found': self.issues_found,
            'recommendations': self.recommendations,
            'department': self.department,
            'is_verified': self.is_verified,
            'helpful_count': self.helpful_count,
            'unhelpful_count': self.unhelpful_count,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
