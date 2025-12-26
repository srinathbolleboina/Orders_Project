"""
Authentication Routes - Login, Registration, User Profile
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from app import db
from app.models.user import User
from app.middleware.auth import token_required, get_current_user
import logging

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
logger = logging.getLogger(__name__)


@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role='user'  # Default role
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"New user registered: {user.email}")
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is inactive'}), 403
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        logger.info(f"User logged in: {user.email}")
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500


@bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get current user profile"""
    try:
        user = get_current_user()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        return jsonify({'error': 'Failed to get profile', 'message': str(e)}), 500


@bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update current user profile"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'password' in data:
            user.set_password(data['password'])
        
        db.session.commit()
        
        logger.info(f"Profile updated: {user.email}")
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update profile error: {str(e)}")
        return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500
