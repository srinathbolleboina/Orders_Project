"""
Order Model - Manages customer orders
"""
from datetime import datetime
from app import db


class Order(db.Model):
    """Order model for order management"""
    
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, processing, shipped, delivered, cancelled
    shipping_address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self, include_items=True):
        """Convert order to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'shipping_address': self.shipping_address,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_items:
            data['items'] = [item.to_dict() for item in self.order_items]
            data['payment'] = self.payment.to_dict() if self.payment else None
        
        return data
    
    def __repr__(self):
        return f'<Order {self.id} - User:{self.user_id}>'


class OrderItem(db.Model):
    """Order item model for individual items in an order"""
    
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)  # Store price at time of purchase
    
    def to_dict(self):
        """Convert order item to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'price_at_purchase': self.price_at_purchase,
            'subtotal': self.price_at_purchase * self.quantity
        }
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'
