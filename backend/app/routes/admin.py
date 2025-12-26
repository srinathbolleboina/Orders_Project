"""
Admin Routes - Admin dashboard and management
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.payment import Payment
from app.middleware.auth import admin_required
from sqlalchemy import func
import logging

bp = Blueprint('admin', __name__, url_prefix='/api/admin')
logger = logging.getLogger(__name__)


@bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard():
    """Get admin dashboard statistics"""
    try:
        # Get statistics
        total_users = User.query.filter_by(role='user').count()
        total_products = Product.query.filter_by(is_active=True).count()
        total_orders = Order.query.count()
        
        # Revenue statistics
        total_revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.status.in_(['processing', 'shipped', 'delivered'])
        ).scalar() or 0
        
        pending_orders = Order.query.filter_by(status='pending').count()
        
        # Recent orders
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
        
        return jsonify({
            'statistics': {
                'total_users': total_users,
                'total_products': total_products,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'pending_orders': pending_orders
            },
            'recent_orders': [order.to_dict(include_items=False) for order in recent_orders]
        }), 200
        
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        return jsonify({'error': 'Failed to get dashboard data', 'message': str(e)}), 500


@bp.route('/orders', methods=['GET'])
@admin_required
def get_all_orders():
    """Get all orders (admin view)"""
    try:
        status = request.args.get('status')
        
        query = Order.query
        
        if status:
            query = query.filter_by(status=status)
        
        orders = query.order_by(Order.created_at.desc()).all()
        
        return jsonify({
            'orders': [order.to_dict() for order in orders],
            'count': len(orders)
        }), 200
        
    except Exception as e:
        logger.error(f"Get all orders error: {str(e)}")
        return jsonify({'error': 'Failed to get orders', 'message': str(e)}), 500


@bp.route('/orders/<int:order_id>/status', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    """Update order status (admin only)"""
    try:
        order = db.session.get(Order, order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
            return jsonify({'error': 'Invalid status'}), 400
        
        order.status = new_status
        db.session.commit()
        
        logger.info(f"Order status updated: {order_id} -> {new_status}")
        
        return jsonify({
            'message': 'Order status updated',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update order status error: {str(e)}")
        return jsonify({'error': 'Failed to update order status', 'message': str(e)}), 500


@bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users (admin view)"""
    try:
        users = User.query.all()
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'count': len(users)
        }), 200
        
    except Exception as e:
        logger.error(f"Get all users error: {str(e)}")
        return jsonify({'error': 'Failed to get users', 'message': str(e)}), 500


@bp.route('/users/<int:user_id>/toggle', methods=['PUT'])
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status (admin only)"""
    try:
        user = db.session.get(User, user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.role == 'admin':
            return jsonify({'error': 'Cannot modify admin users'}), 403
        
        user.is_active = not user.is_active
        db.session.commit()
        
        logger.info(f"User status toggled: {user_id} -> {user.is_active}")
        
        return jsonify({
            'message': 'User status updated',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Toggle user status error: {str(e)}")
        return jsonify({'error': 'Failed to update user status', 'message': str(e)}), 500


@bp.route('/payments', methods=['GET'])
@admin_required
def get_all_payments():
    """Get all payments (admin view)"""
    try:
        payments = Payment.query.order_by(Payment.created_at.desc()).all()
        
        return jsonify({
            'payments': [payment.to_dict() for payment in payments],
            'count': len(payments)
        }), 200
        
    except Exception as e:
        logger.error(f"Get all payments error: {str(e)}")
        return jsonify({'error': 'Failed to get payments', 'message': str(e)}), 500
