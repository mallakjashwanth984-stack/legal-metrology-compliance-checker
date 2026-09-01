from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from models.product import Product
from models.product_image import ProductImage, ImageType
from models.declaration import Declaration
from services.image_processor import ImageProcessor
from services.compliance_checker import ComplianceChecker
import os
from datetime import datetime

product_images_bp = Blueprint('product_images', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@product_images_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_product_images():
    user_id = get_jwt_identity()
    
    # Get product_id from form
    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({'error': 'product_id is required'}), 400
    
    # Verify product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Process each image type
    uploaded_images = {}
    image_types = ['front', 'back', 'side', 'top', 'bottom']
    
    for image_type in image_types:
        if image_type not in request.files:
            continue
        
        file = request.files[image_type]
        
        if file.filename == '':
            continue
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'Invalid file type for {image_type}. Allowed: png, jpg, jpeg, gif, bmp'}), 400
        
        # Save file
        filename = secure_filename(f"{product_id}_{image_type}_{datetime.utcnow().timestamp()}_{file.filename}")
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'product_images')
        os.makedirs(upload_path, exist_ok=True)
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        # Process image and extract text
        image_processor = ImageProcessor()
        extracted_data = image_processor.process_image(file_path)
        
        # Create product image record
        product_image = ProductImage(
            product_id=product_id,
            image_type=ImageType[image_type.upper()],
            image_path=file_path,
            extracted_text=extracted_data.get('raw_text'),
            image_quality_score=extracted_data.get('image_quality', {}).get('quality_score', 0),
            uploaded_by=user_id
        )
        
        db.session.add(product_image)
        db.session.flush()
        
        uploaded_images[image_type] = {
            'id': product_image.id,
            'image_type': image_type,
            'extracted_data': extracted_data
        }
    
    if not uploaded_images:
        return jsonify({'error': 'No images were uploaded'}), 400
    
    db.session.commit()
    
    return jsonify({
        'message': 'Product images uploaded successfully',
        'product_id': product_id,
        'uploaded_images': uploaded_images
    }), 201

@product_images_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product_images(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    images = ProductImage.query.filter_by(product_id=product_id).all()
    
    return jsonify({
        'product_id': product_id,
        'total_images': len(images),
        'images': [img.to_dict() for img in images]
    }), 200

@product_images_bp.route('/<int:image_id>', methods=['GET'])
@jwt_required()
def get_product_image(image_id):
    image = ProductImage.query.get(image_id)
    
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    
    return jsonify(image.to_dict()), 200

@product_images_bp.route('/<int:image_id>', methods=['DELETE'])
@jwt_required()
def delete_product_image(image_id):
    user_id = get_jwt_identity()
    image = ProductImage.query.get(image_id)
    
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    
    # Only allow deletion by uploader or admin
    if image.uploaded_by != user_id:
        return jsonify({'error': 'Unauthorized to delete this image'}), 403
    
    # Delete file
    if os.path.exists(image.image_path):
        os.remove(image.image_path)
    
    db.session.delete(image)
    db.session.commit()
    
    return jsonify({'message': 'Image deleted successfully'}), 200

@product_images_bp.route('/by-type/<int:product_id>/<image_type>', methods=['GET'])
@jwt_required()
def get_product_image_by_type(product_id, image_type):
    try:
        img_type = ImageType[image_type.upper()]
    except KeyError:
        return jsonify({'error': f'Invalid image type. Allowed: front, back, side, top, bottom'}), 400
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    image = ProductImage.query.filter_by(
        product_id=product_id,
        image_type=img_type
    ).first()
    
    if not image:
        return jsonify({'error': f'No {image_type} image found for this product'}), 404
    
    return jsonify(image.to_dict()), 200
