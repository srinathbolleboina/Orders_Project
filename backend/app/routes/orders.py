"""
Order Routes - Order management and processing
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.product import Product
from app.models.payment import Payment
from app.middleware.auth import token_required, admin_required, get_current_user
import logging
import uuid

bp = Blueprint('orders', __name__, url_prefix='/api/orders')
logger = logging.getLogger(__name__)


@bp.route('', methods=['GET'])
@token_required
def get_orders():
    """Get user's orders"""
    try:
        user = get_current_user()
        orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
        
        return jsonify({
            'orders': [order.to_dict() for order in orders],
            'count': len(orders)
        }), 200
        
    except Exception as e:
        logger.error(f"Get orders error: {str(e)}")
        return jsonify({'error': 'Failed to get orders', 'message': str(e)}), 500


@bp.route('/<int:order_id>', methods=['GET'])
@token_required
def get_order(order_id):
    """Get single order details"""
    try:
        user = get_current_user()
        order = Order.query.filter_by(id=order_id, user_id=user.id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({'order': order.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Get order error: {str(e)}")
        return jsonify({'error': 'Failed to get order', 'message': str(e)}), 500


@bp.route('/checkout', methods=['POST'])
@token_required
def checkout():
    """Create order from cart items"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        # Get cart items
        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate total and validate stock
        total_amount = 0
        for item in cart_items:
            if not item.product or not item.product.is_active:
                return jsonify({'error': f'Product {item.product_id} not available'}), 400
            
            if item.product.stock_quantity < item.quantity:
                return jsonify({'error': f'Insufficient stock for {item.product.name}'}), 400
            
            total_amount += item.product.price * item.quantity
        
        # Create order
        order = Order(
            user_id=user.id,
            total_amount=total_amount,
            status='pending',
            shipping_address=data.get('shipping_address', '')
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items and update stock
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )
            db.session.add(order_item)
            
            # Update product stock
            item.product.stock_quantity -= item.quantity
        
        # Create payment record
        payment = Payment(
            order_id=order.id,
            amount=total_amount,
            payment_method=data.get('payment_method', 'credit_card'),
            payment_status='completed',  # Simulated payment
            transaction_id=str(uuid.uuid4())
        )
        db.session.add(payment)
        
        # Update order status
        order.status = 'processing'
        
        # Clear cart
        CartItem.query.filter_by(user_id=user.id).delete()
        
        db.session.commit()
        
        logger.info(f"Order created: {order.id} for user {user.id}")
        
        return jsonify({
            'message': 'Order placed successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Checkout error: {str(e)}")
        return jsonify({'error': 'Failed to create order', 'message': str(e)}), 500


@bp.route('/<int:order_id>/cancel', methods=['POST'])
@token_required
def cancel_order(order_id):
    """Cancel an order"""
    try:
        user = get_current_user()
        order = Order.query.filter_by(id=order_id, user_id=user.id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order.status not in ['pending', 'processing']:
            return jsonify({'error': 'Order cannot be cancelled'}), 400
        
        # Restore stock
        for item in order.order_items:
            if item.product:
                item.product.stock_quantity += item.quantity
        
        # Update order and payment status
        order.status = 'cancelled'
        if order.payment:
            order.payment.payment_status = 'refunded'
        
        db.session.commit()
        
        logger.info(f"Order cancelled: {order_id}")
        
        return jsonify({'message': 'Order cancelled successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Cancel order error: {str(e)}")
        return jsonify({'error': 'Failed to cancel order', 'message': str(e)}), 500
