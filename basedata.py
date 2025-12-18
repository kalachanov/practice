from flask_sqlalchemy import SQLAlchemy
from config import CONFIG
from datetime import datetime
db = SQLAlchemy()

class init_database:
    
    def __init__(self, app=None):
        """Инициализация базы данных"""
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация приложения Flask"""
        app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG.SQLALCHEMY_TRACK_MODIFICATIONS
        
        db.init_app(app)
        
        with app.app_context():
            db.create_all()
            

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    FirstName = db.Column(db.String(20))
    SecondName = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __init__(self, username, email, phone, password):
        self.username = username
        self.email = email
        self.phone = phone
        self.password = password
        
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    def __repr__(self):
        return f'<Category {self.name}>'

class Second_Category(db.Model):
    __tablename__ = 'second_categories'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    id_categories = db.Column(db.Integer, db.ForeignKey(Category.id))
    category = db.relationship('Category', backref='second_categories', lazy='dynamic')
    
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    def __repr__(self):
        return f'<Second_Category {self.name}>'
    
class Third_Category(db.Model):
    __tablename__ = 'third_categories'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    id_second_categories = db.Column(db.Integer, db.ForeignKey(Second_Category.id))
    category = db.relationship('Second_Category', backref='third_categories', lazy='dynamic')
    
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    def __repr__(self):
        return f'<Third_Category {self.name}>'
    
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    id_third_categories = db.Column(db.Integer, db.ForeignKey(Third_Category.id))
    third_categories = db.relationship('Third_Category', backref='products', lazy='dynamic')
        
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    characteristics = db.Column(db.Text)
    photo = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __init__(self, name, description=None, characteristics=None, photo=None, quantity=None):
        self.name = name
        self.description = description
        self.characteristics = characteristics
        self.photo = photo
        self.quantity = quantity
        
    def __repr__(self):
        return f'<Product {self.name}>'
    
class Favorite:
    __tablename__ = 'favorites'
    pass
class Favorite_Product(db.Model):
    __tablename__ = 'favorites_products'
    pass
class Cars(db.Model):
    __tablename__ = 'cars'
    pass
class Cars_Product(db.Model):
    __tablename__ = 'cars_products'
    pass
class Comment(db.Model):
    __tablename__ = 'comments'
    pass

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    
    database = init_database(app)
    
    # Теперь можно работать с БД в контексте приложения
    with app.app_context():
        
        print(User.query.all())