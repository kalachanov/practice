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
    pass
class Product(db.Model):
    pass
class Category(db.Model):
    pass
class Second_Category(db.Model):
    pass
class Third_Category(db.Model):
    pass
class Favorite:
    pass
class Favorite_Product(db.Model):
    pass
class Cars(db.Model):
    pass
class Cars_Product(db.Model):
    pass
class Comment(db.Model):
    pass

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    
    database = DataBase(app)
    
    # Теперь можно работать с БД в контексте приложения
    with app.app_context():
        
        print(User.query.all())