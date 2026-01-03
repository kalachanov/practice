from flask_sqlalchemy import SQLAlchemy
from config import CONFIG
from datetime import datetime

db = SQLAlchemy()

class DatabaseManager:
    """
    Менеджер для инициализации базы данных
    """
    
    def __init__(self, app=None):
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
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    email = db.Column(db.String(50), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Для хэшированных паролей
    first_name = db.Column(db.String(20))
    second_name = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Отношения
    favorites = db.relationship('FavoriteProduct', backref='user', lazy=True, 
                               cascade='all, delete-orphan')
    cart_items = db.relationship('CartProduct', backref='user', lazy=True,
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy=True,
                              cascade='all, delete-orphan')
    
    def __init__(self, username, email, phone, password, first_name=None, second_name=None):
        self.username = username
        self.email = email
        self.phone = phone
        self.password = password
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
    
    def __init__(self, name, description):
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
    
    def __init__(self, name, description, category_id):
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
    
    def __init__(self, name, description, second_category_id):
        self.name = name
        self.description = description
        self.second_category_id = second_category_id
        
    def __repr__(self):
        return f'<ThirdCategory {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = (
        db.CheckConstraint('quantity >= 0', name='check_quantity_positive'),
    )
    
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
    
    def __init__(self, name, third_category_id=None, description=None, 
                 characteristics=None, photo=None, quantity=0):
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
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_favorite'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id
        
    def __repr__(self):
        return f'<FavoriteProduct user:{self.user_id} product:{self.product_id}>'


class CartProduct(db.Model):
    __tablename__ = 'cart_products'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_cart_item'),
        db.CheckConstraint('quantity > 0', name='check_cart_quantity_positive'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, product_id, quantity=1):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        
    def __repr__(self):
        return f'<CartProduct user:{self.user_id} product:{self.product_id} qty:{self.quantity}>'


class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, product_id, text):
        self.user_id = user_id
        self.product_id = product_id
        self.text = text
        
    def __repr__(self):
        return f'<Comment user:{self.user_id} product:{self.product_id}>'


if __name__ == "__main__":
    from flask import Flask
    
    app = Flask(__name__)
    
    # Для тестирования используем временную базу данных
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("База данных успешно создана!")
        
        # Пример добавления тестовых данных
        try:
            # Создаем категории
            category = Category(name="Электроника", description="Электронные устройства")
            db.session.add(category)
            db.session.commit()
            
            second_category = SecondCategory(name="Смартфоны", description="Мобильные телефоны", category_id=category.id)
            db.session.add(second_category)
            db.session.commit()
            
            third_category = ThirdCategory(name="Android", description="Смартфоны на Android", 
                                          second_category_id=second_category.id)
            db.session.add(third_category)
            db.session.commit()
            
            # Создаем продукт
            product = Product(
                name="Samsung Galaxy S23",
                third_category_id=third_category.id,
                description="Флагманский смартфон",
                characteristics='{"ram": "8GB", "storage": "256GB"}',
                photo="/images/galaxy_s23.jpg",
                quantity=10
            )
            db.session.add(product)
            db.session.commit()
            
            print("Тестовые данные добавлены успешно!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при добавлении тестовых данных: {e}")