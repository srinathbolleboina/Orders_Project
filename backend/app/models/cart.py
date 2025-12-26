"""
Cart Model - Manages shopping cart items
"""
from datetime import datetime
from app import db


class CartItem(db.Model):
    """Cart item model for shopping cart management"""
    
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert cart item to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'subtotal': self.product.price * self.quantity if self.product else 0,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<CartItem User:{self.user_id} Product:{self.product_id}>'
