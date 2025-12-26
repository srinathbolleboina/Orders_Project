"""
Orders Application - Backend Package
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config
import logging

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Configure logging
    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register blueprints
    from app.routes import auth, products, cart, orders, admin, health
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(health.bp)
    
    return app
