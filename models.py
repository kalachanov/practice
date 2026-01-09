from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    email = db.Column(db.String(50), unique=True, index=True)
    phone = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(255), nullable=False)  # Для хэшированных паролей
    first_name = db.Column(db.String(20))
    second_name = db.Column(db.String(20))
    admin = db.Column(db.Integer(1))
    mute = db.Column(db.Integer(1))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    favorites = db.relationship('FavoriteProduct', backref='user', lazy=True, 
                               cascade='all, delete-orphan')
    cart_items = db.relationship('CartProduct', backref='user', lazy=True,
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy=True,
                              cascade='all, delete-orphan')
    
    def __init__(self, username: str, password: str, first_name: str = None, 
                 second_name: str = None, email: str = None, phone: str = None):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.first_name = first_name
        self.second_name = second_name
        
    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    
    # Отношения
    second_categories = db.relationship('SecondCategory', backref='category', lazy=True,
                                       cascade='all, delete-orphan')
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        
    def __repr__(self):
        return f'<Category {self.name}>'


class SecondCategory(db.Model):
    __tablename__ = 'second_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(80), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    
    # Отношения
    third_categories = db.relationship('ThirdCategory', backref='second_category', lazy=True,
                                      cascade='all, delete-orphan')
    
    def __init__(self, name: str, description: str, category_id: int):
        self.name = name
        self.description = description
        self.category_id = category_id
        
    def __repr__(self):
        return f'<SecondCategory {self.name}>'


class ThirdCategory(db.Model):
    __tablename__ = 'third_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    second_category_id = db.Column(db.Integer, db.ForeignKey('second_categories.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(80), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    
    # Отношения
    products = db.relationship('Product', backref='third_category', lazy=True,
                              cascade='all, delete-orphan')
    
    def __init__(self, name: str, description: str, second_category_id: int):
        self.name = name
        self.description = description
        self.second_category_id = second_category_id
        
    def __repr__(self):
        return f'<ThirdCategory {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    third_category_id = db.Column(db.Integer, db.ForeignKey('third_categories.id', ondelete='SET NULL'))
    name = db.Column(db.String(80), nullable=False, index=True)
    description = db.Column(db.Text)
    characteristics = db.Column(db.Text)  # JSON или обычный текст
    photo = db.Column(db.Text)  # URL или путь к файлу
    quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Отношения
    favorites = db.relationship('FavoriteProduct', backref='product', lazy=True,
                               cascade='all, delete-orphan')
    cart_items = db.relationship('CartProduct', backref='product', lazy=True,
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='product', lazy=True,
                              cascade='all, delete-orphan')
    
    def __init__(self, name: str, third_category_id: int, description: str = None, 
                 characteristics: str = None, photo: str = None, quantity: int = 0):
        self.name = name
        self.third_category_id = third_category_id
        self.description = description
        self.characteristics = characteristics
        self.photo = photo
        self.quantity = quantity
        
    def __repr__(self):
        return f'<Product {self.name}>'


class FavoriteProduct(db.Model):
    __tablename__ = 'favorite_products'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __init__(self, user_id: int, product_id: int):
        self.user_id = user_id
        self.product_id = product_id
        
    def __repr__(self):
        return f'<FavoriteProduct user:{self.user_id} product:{self.product_id}>'


class CartProduct(db.Model):
    __tablename__ = 'cart_products'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __init__(self, user_id: int, product_id: int):
        self.user_id = user_id
        self.product_id = product_id
        
    def __repr__(self):
        return f'<CartProduct user:{self.user_id} product:{self.product_id}>'


class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __init__(self, user_id: int, product_id: int, text: str):
        self.user_id = user_id
        self.product_id = product_id
        self.text = text
        
    def __repr__(self):
        return f'<Comment user:{self.user_id} product:{self.product_id}>'
