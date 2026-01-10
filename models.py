from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    wishlists = db.relationship('Wishlist', backref='user', lazy=True, cascade='all, delete-orphan')
    carts = db.relationship('Cart', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Category(db.Model):
    """Product categories"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    """Product model"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    wishlists = db.relationship('Wishlist', backref='product', lazy=True, cascade='all, delete-orphan')
    carts = db.relationship('Cart', backref='product', lazy=True, cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'


class Wishlist(db.Model):
    """User wishlist"""
    __tablename__ = 'wishlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate wishlist entries
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_wishlist'),)
    
    def __repr__(self):
        return f'<Wishlist User:{self.user_id} Product:{self.product_id}>'


class Cart(db.Model):
    """Shopping cart"""
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate cart entries
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_cart'),)
    
    def __repr__(self):
        return f'<Cart User:{self.user_id} Product:{self.product_id} Qty:{self.quantity}>'


class Order(db.Model):
    """Customer orders"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    
    # Shipping information
    shipping_name = db.Column(db.String(100))
    shipping_email = db.Column(db.String(120))
    shipping_address = db.Column(db.Text)
    shipping_city = db.Column(db.String(100))
    shipping_postal_code = db.Column(db.String(20))
    shipping_country = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(db.Model):
    """Individual items in an order"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price at time of purchase
    
    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} Product:{self.product_id}>'
