"""
Test Configuration
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.product import Product


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return headers"""
    # Create test user
    user = User(
        email='test@example.com',
        first_name='Test',
        last_name='User',
        role='user'
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    
    # Login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def admin_headers(client):
    """Create admin user and return headers"""
    # Create admin user
    admin = User(
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    
    # Login
    response = client.post('/api/auth/login', json={
        'email': 'admin@example.com',
        'password': 'admin123'
    })
    
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def sample_product():
    """Create sample product"""
    product = Product(
        name='Test Product',
        description='Test Description',
        price=99.99,
        stock_quantity=10,
        category='Test'
    )
    db.session.add(product)
    db.session.commit()
    return product
