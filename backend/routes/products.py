from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from models.product import Product
from models.declaration import Declaration
from models.violation import Violation
from services.image_processor import ImageProcessor
from services.compliance_checker import ComplianceChecker
import os

products_bp = Blueprint('products', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@products_bp.route('/', methods=['GET'])
@jwt_required()
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Product.query
    
    if search:
        query = query.filter(Product.product_name.ilike(f'%{search}%'))
    if category:
        query = query.filter_by(product_category=category)
    
    products = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': products.total,
        'pages': products.pages,
        'current_page': page,
        'products': [product.to_dict() for product in products.items]
    }), 200

@products_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    product_data = product.to_dict()
    product_data['declarations'] = [d.to_dict() for d in product.declarations]
    product_data['violations'] = [v.to_dict() for v in product.violations]
    
    return jsonify(product_data), 200

@products_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_product():
    user_id = get_jwt_identity()
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, bmp'}), 400
    
    filename = secure_filename(file.filename)
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products')
    os.makedirs(upload_path, exist_ok=True)
    file_path = os.path.join(upload_path, filename)
    file.save(file_path)
    
    # Process image and extract text
    image_processor = ImageProcessor()
    extracted_data = image_processor.process_image(file_path)
    
    # Create product record
    product = Product(
        product_name=request.form.get('product_name', 'Unknown Product'),
        product_category=request.form.get('category', 'General'),
        manufacturer_name=extracted_data.get('manufacturer_name'),
        image_path=file_path,
        created_by=user_id
    )
    
    db.session.add(product)
    db.session.flush()
    
    # Store extracted declarations
    for decl_type, decl_data in extracted_data.get('declarations', {}).items():
        declaration = Declaration(
            product_id=product.id,
            declaration_type=decl_type,
            extracted_text=decl_data.get('text'),
            font_size=decl_data.get('font_size'),
            position=decl_data.get('position'),
            confidence_score=decl_data.get('confidence')
        )
        db.session.add(declaration)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Product uploaded successfully',
        'product': product.to_dict(),
        'extracted_data': extracted_data
    }), 201

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Delete image file
    if product.image_path and os.path.exists(product.image_path):
        os.remove(product.image_path)
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted successfully'}), 200
