from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.product import Product
from models.product_review import ProductReview, ReviewRating
from models.user import User
from datetime import datetime
from sqlalchemy import func, or_

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/<int:product_id>', methods=['POST'])
@jwt_required()
def create_review(product_id):
    user_id = get_jwt_identity()
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Check if user already reviewed this product
    existing_review = ProductReview.query.filter_by(
        product_id=product_id,
        user_id=user_id
    ).first()
    
    if existing_review:
        return jsonify({'error': 'You have already reviewed this product'}), 400
    
    data = request.get_json()
    
    if not data.get('rating'):
        return jsonify({'error': 'Rating is required'}), 400
    
    try:
        rating = ReviewRating(int(data.get('rating')))
    except ValueError:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    user = User.query.get(user_id)
    
    review = ProductReview(
        product_id=product_id,
        user_id=user_id,
        rating=rating,
        title=data.get('title'),
        review_text=data.get('review_text'),
        compliance_feedback=data.get('compliance_feedback'),  # 'compliant', 'non_compliant', 'needs_improvement'
        issues_found=data.get('issues_found'),  # Array of issues
        recommendations=data.get('recommendations'),
        department=user.department,
        is_verified=data.get('is_verified', False),
        status='pending'  # Will be approved by admin
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({
        'message': 'Review submitted successfully',
        'review': review.to_dict()
    }), 201

@reviews_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product_reviews(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status_filter = request.args.get('status', 'approved')  # Default to approved reviews
    
    query = ProductReview.query.filter_by(product_id=product_id, status=status_filter)
    
    reviews = query.order_by(ProductReview.created_at.desc()).paginate(
        page=page, per_page=per_page
    )
    
    # Calculate average rating for product
    avg_rating = db.session.query(func.avg(func.cast(ProductReview.rating, db.Integer))).filter_by(
        product_id=product_id,
        status='approved'
    ).scalar()
    
    review_count = ProductReview.query.filter_by(
        product_id=product_id,
        status='approved'
    ).count()
    
    return jsonify({
        'product_id': product_id,
        'total_reviews': reviews.total,
        'pages': reviews.pages,
        'current_page': page,
        'average_rating': round(avg_rating, 2) if avg_rating else 0,
        'review_count': review_count,
        'reviews': [review.to_dict() for review in reviews.items]
    }), 200

@reviews_bp.route('/<int:review_id>', methods=['GET'])
@jwt_required()
def get_review(review_id):
    review = ProductReview.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    return jsonify(review.to_dict()), 200

@reviews_bp.route('/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    user_id = get_jwt_identity()
    review = ProductReview.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    # Only allow update by reviewer
    if review.user_id != user_id:
        return jsonify({'error': 'Unauthorized to update this review'}), 403
    
    data = request.get_json()
    
    if 'rating' in data:
        try:
            review.rating = ReviewRating(int(data['rating']))
        except ValueError:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    if 'title' in data:
        review.title = data['title']
    if 'review_text' in data:
        review.review_text = data['review_text']
    if 'compliance_feedback' in data:
        review.compliance_feedback = data['compliance_feedback']
    if 'issues_found' in data:
        review.issues_found = data['issues_found']
    if 'recommendations' in data:
        review.recommendations = data['recommendations']
    
    review.updated_at = datetime.utcnow()
    review.status = 'pending'  # Reset to pending for re-approval
    
    db.session.commit()
    
    return jsonify({
        'message': 'Review updated successfully',
        'review': review.to_dict()
    }), 200

@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    user_id = get_jwt_identity()
    review = ProductReview.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    # Only allow deletion by reviewer
    if review.user_id != user_id:
        return jsonify({'error': 'Unauthorized to delete this review'}), 403
    
    db.session.delete(review)
    db.session.commit()
    
    return jsonify({'message': 'Review deleted successfully'}), 200

@reviews_bp.route('/<int:review_id>/approve', methods=['PUT'])
@jwt_required()
def approve_review(review_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Only admins can approve
    if user.role != 'admin':
        return jsonify({'error': 'Only administrators can approve reviews'}), 403
    
    review = ProductReview.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    review.status = 'approved'
    review.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Review approved successfully',
        'review': review.to_dict()
    }), 200

@reviews_bp.route('/<int:review_id>/reject', methods=['PUT'])
@jwt_required()
def reject_review(review_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Only admins can reject
    if user.role != 'admin':
        return jsonify({'error': 'Only administrators can reject reviews'}), 403
    
    review = ProductReview.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    review.status = 'rejected'
    review.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Review rejected successfully',
        'review': review.to_dict()
    }), 200

@reviews_bp.route('/<int:review_id>/helpful', methods=['PUT'])
@jwt_required()
def mark_helpful(review_id):
    review = ProductReview.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    review.helpful_count += 1
    db.session.commit()
    
    return jsonify({
        'message': 'Marked as helpful',
        'helpful_count': review.helpful_count
    }), 200

@reviews_bp.route('/<int:review_id>/unhelpful', methods=['PUT'])
@jwt_required()
def mark_unhelpful(review_id):
    review = ProductReview.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    review.unhelpful_count += 1
    db.session.commit()
    
    return jsonify({
        'message': 'Marked as unhelpful',
        'unhelpful_count': review.unhelpful_count
    }), 200

@reviews_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_reviews(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    reviews = ProductReview.query.filter_by(user_id=user_id).order_by(
        ProductReview.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'user_id': user_id,
        'total_reviews': reviews.total,
        'pages': reviews.pages,
        'current_page': page,
        'reviews': [review.to_dict() for review in reviews.items]
    }), 200

@reviews_bp.route('/compliance-summary/<int:product_id>', methods=['GET'])
@jwt_required()
def get_compliance_summary(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    reviews = ProductReview.query.filter_by(
        product_id=product_id,
        status='approved'
    ).all()
    
    compliant_count = len([r for r in reviews if r.compliance_feedback == 'compliant'])
    non_compliant_count = len([r for r in reviews if r.compliance_feedback == 'non_compliant'])
    needs_improvement_count = len([r for r in reviews if r.compliance_feedback == 'needs_improvement'])
    
    compliance_percentage = 0
    if len(reviews) > 0:
        compliance_percentage = round((compliant_count / len(reviews)) * 100, 2)
    
    return jsonify({
        'product_id': product_id,
        'total_reviews': len(reviews),
        'compliant': compliant_count,
        'non_compliant': non_compliant_count,
        'needs_improvement': needs_improvement_count,
        'compliance_percentage': compliance_percentage,
        'common_issues': self._get_common_issues(reviews),
        'top_recommendations': self._get_top_recommendations(reviews)
    }), 200

def _get_common_issues(reviews):
    from collections import Counter
    all_issues = []
    for review in reviews:
        if review.issues_found:
            all_issues.extend(review.issues_found)
    
    counter = Counter(all_issues)
    return dict(counter.most_common(5))

def _get_top_recommendations(reviews):
    from collections import Counter
    recommendations = []
    for review in reviews:
        if review.recommendations:
            recommendations.append(review.recommendations)
    
    return recommendations[:5]
