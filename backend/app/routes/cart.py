"""
Cart Routes - Shopping cart management
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.cart import CartItem
from app.models.product import Product
from app.middleware.auth import token_required, get_current_user
import logging

bp = Blueprint('cart', __name__, url_prefix='/api/cart')
logger = logging.getLogger(__name__)


@bp.route('', methods=['GET'])
@token_required
def get_cart():
    """Get user's cart items"""
    try:
        user = get_current_user()
        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        
        total = sum(item.product.price * item.quantity for item in cart_items if item.product)
        
        return jsonify({
            'cart_items': [item.to_dict() for item in cart_items],
            'total': total,
            'count': len(cart_items)
        }), 200
        
    except Exception as e:
        logger.error(f"Get cart error: {str(e)}")
        return jsonify({'error': 'Failed to get cart', 'message': str(e)}), 500


@bp.route('/add', methods=['POST'])
@token_required
def add_to_cart():
    """Add item to cart"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if 'product_id' not in data:
            return jsonify({'error': 'Product ID required'}), 400
        
        product_id = data['product_id']
        quantity = data.get('quantity', 1)
        
        # Check if product exists and is active
        product = db.session.get(Product, product_id)
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check stock
        if product.stock_quantity < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        # Check if item already in cart
        cart_item = CartItem.query.filter_by(
            user_id=user.id,
            product_id=product_id
        ).first()
        
        if cart_item:
            # Update quantity
            cart_item.quantity += quantity
        else:
            # Create new cart item
            cart_item = CartItem(
                user_id=user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        logger.info(f"Item added to cart: User {user.id}, Product {product_id}")
        
        return jsonify({
            'message': 'Item added to cart',
            'cart_item': cart_item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Add to cart error: {str(e)}")
        return jsonify({'error': 'Failed to add to cart', 'message': str(e)}), 500


@bp.route('/<int:cart_item_id>', methods=['PUT'])
@token_required
def update_cart_item(cart_item_id):
    """Update cart item quantity"""
    try:
        user = get_current_user()
        cart_item = CartItem.query.filter_by(
            id=cart_item_id,
            user_id=user.id
        ).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        data = request.get_json()
        quantity = data.get('quantity', 1)
        
        # Check stock
        if cart_item.product.stock_quantity < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        cart_item.quantity = quantity
        db.session.commit()
        
        logger.info(f"Cart item updated: {cart_item_id}")
        
        return jsonify({
            'message': 'Cart item updated',
            'cart_item': cart_item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update cart error: {str(e)}")
        return jsonify({'error': 'Failed to update cart', 'message': str(e)}), 500


@bp.route('/<int:cart_item_id>', methods=['DELETE'])
@token_required
def remove_from_cart(cart_item_id):
    """Remove item from cart"""
    try:
        user = get_current_user()
        cart_item = CartItem.query.filter_by(
            id=cart_item_id,
            user_id=user.id
        ).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        logger.info(f"Cart item removed: {cart_item_id}")
        
        return jsonify({'message': 'Item removed from cart'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Remove from cart error: {str(e)}")
        return jsonify({'error': 'Failed to remove from cart', 'message': str(e)}), 500


@bp.route('/clear', methods=['DELETE'])
@token_required
def clear_cart():
    """Clear all items from cart"""
    try:
        user = get_current_user()
        CartItem.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        
        logger.info(f"Cart cleared for user: {user.id}")
        
        return jsonify({'message': 'Cart cleared'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Clear cart error: {str(e)}")
        return jsonify({'error': 'Failed to clear cart', 'message': str(e)}), 500
