"""
Database initialization and seeding script
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.product import Product
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from config import Config


def init_database():
    """Initialize the database and create tables"""
    app = create_app('development')
    
    with app.app_context():
        # Drop all tables and recreate (for development)
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating database tables...")
        db.create_all()
        
        print("Database tables created successfully!")
        
        # Create admin user
        print("Creating admin user...")
        admin = User(
            email=Config.ADMIN_EMAIL,
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        admin.set_password(Config.ADMIN_PASSWORD)
        db.session.add(admin)
        
        # Create test user
        print("Creating test user...")
        test_user = User(
            email='user@orders.com',
            first_name='Test',
            last_name='User',
            role='user'
        )
        test_user.set_password('user123')
        db.session.add(test_user)
        
        # Create sample products
        print("Creating sample products...")
        products = [
            Product(
                name='Laptop',
                description='High-performance laptop for professionals',
                price=999.99,
                stock_quantity=50,
                category='Electronics',
                image_url='https://via.placeholder.com/300x300?text=Laptop'
            ),
            Product(
                name='Wireless Mouse',
                description='Ergonomic wireless mouse with precision tracking',
                price=29.99,
                stock_quantity=200,
                category='Electronics',
                image_url='https://via.placeholder.com/300x300?text=Mouse'
            ),
            Product(
                name='Mechanical Keyboard',
                description='RGB mechanical keyboard with blue switches',
                price=89.99,
                stock_quantity=100,
                category='Electronics',
                image_url='https://via.placeholder.com/300x300?text=Keyboard'
            ),
            Product(
                name='USB-C Hub',
                description='7-in-1 USB-C hub with HDMI and card reader',
                price=49.99,
                stock_quantity=150,
                category='Accessories',
                image_url='https://via.placeholder.com/300x300?text=USB-Hub'
            ),
            Product(
                name='Webcam HD',
                description='1080p HD webcam with auto-focus',
                price=79.99,
                stock_quantity=75,
                category='Electronics',
                image_url='https://via.placeholder.com/300x300?text=Webcam'
            ),
            Product(
                name='Desk Lamp',
                description='LED desk lamp with adjustable brightness',
                price=34.99,
                stock_quantity=120,
                category='Office',
                image_url='https://via.placeholder.com/300x300?text=Lamp'
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        # Commit all changes
        db.session.commit()
        print("Sample data created successfully!")
        print(f"\nAdmin credentials: {Config.ADMIN_EMAIL} / {Config.ADMIN_PASSWORD}")
        print(f"Test user credentials: user@orders.com / user123")
        print("\nDatabase initialization complete!")


if __name__ == '__main__':
    init_database()
