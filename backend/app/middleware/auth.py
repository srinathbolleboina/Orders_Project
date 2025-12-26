"""
Authentication Middleware
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.models.user import User
from app import db


def token_required(fn):
    """Decorator to require valid JWT token"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid or missing token', 'message': str(e)}), 401
    return wrapper


def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            if user.role != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Authentication failed', 'message': str(e)}), 401
    return wrapper


def get_current_user():
    """Get current authenticated user"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return db.session.get(User, user_id)
    except:
        return None
