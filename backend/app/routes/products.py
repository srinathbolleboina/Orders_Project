"""
Product Routes - Product catalog and management
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product
from app.middleware.auth import token_required, admin_required
import logging

bp = Blueprint('products', __name__, url_prefix='/api/products')
logger = logging.getLogger(__name__)


@bp.route('', methods=['GET'])
def get_products():
    """Get all active products (public endpoint)"""
    try:
        # Get query parameters for filtering
        category = request.args.get('category')
        search = request.args.get('search')
        
        query = Product.query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))
        
        products = query.all()
        
        return jsonify({
            'products': [product.to_dict() for product in products],
            'count': len(products)
        }), 200
        
    except Exception as e:
        logger.error(f"Get products error: {str(e)}")
        return jsonify({'error': 'Failed to get products', 'message': str(e)}), 500


@bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID (public endpoint)"""
    try:
        product = db.session.get(Product, product_id)
        
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'product': product.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Get product error: {str(e)}")
        return jsonify({'error': 'Failed to get product', 'message': str(e)}), 500


@bp.route('', methods=['POST'])
@admin_required
def create_product():
    """Create new product (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create product
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            stock_quantity=data.get('stock_quantity', 0),
            category=data.get('category', ''),
            image_url=data.get('image_url', '')
        )
        
        db.session.add(product)
        db.session.commit()
        
        logger.info(f"Product created: {product.name}")
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Create product error: {str(e)}")
        return jsonify({'error': 'Failed to create product', 'message': str(e)}), 500


@bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    """Update product (admin only)"""
    try:
        product = db.session.get(Product, product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'stock_quantity' in data:
            product.stock_quantity = data['stock_quantity']
        if 'category' in data:
            product.category = data['category']
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'is_active' in data:
            product.is_active = data['is_active']
        
        db.session.commit()
        
        logger.info(f"Product updated: {product.name}")
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update product error: {str(e)}")
        return jsonify({'error': 'Failed to update product', 'message': str(e)}), 500


@bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    """Delete product (soft delete - admin only)"""
    try:
        product = db.session.get(Product, product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Soft delete
        product.is_active = False
        db.session.commit()
        
        logger.info(f"Product deleted: {product.name}")
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Delete product error: {str(e)}")
        return jsonify({'error': 'Failed to delete product', 'message': str(e)}), 500


@bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        categories = db.session.query(Product.category).filter(
            Product.is_active.is_(True),
            Product.category.isnot(None)
        ).distinct().all()

        return jsonify({
            'categories': [cat[0] for cat in categories if cat[0]]
        }), 200

    except Exception as e:
        logger.error(f"Get categories error: {str(e)}")
        return jsonify({'error': 'Failed to get categories', 'message': str(e)}), 500

