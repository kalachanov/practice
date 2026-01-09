from config import CONFIG
from models import *
from flask import Flask

app = Flask(__name__)    
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

class user:
    class bd_user:
        @staticmethod
        def registration(username: str, password: str, first_name: str = None, 
                 second_name: str = None, email: str = None, phone: str = None):
            try:
                user = User(username, password, first_name, 
                 second_name, email, phone)
                db.session.add(user)
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def login(password: str, username: str = None, email: str = None, phone: str = None):
            try:
                if username and User.query\
                    .filter(User.username == username, User.password == password).first():
                    return True
                if email and User.query\
                    .filter(User.email == email, User.password == password).first():
                    return True
                if phone and User.query\
                    .filter(User.phone == phone, User.password == password).first():
                    return True
                else:
                    return False
            except Exception as e:
                return f'Произошла ошибка:\n{e}' 
            
        @staticmethod
        def get_by_username(username: str):
            try:
                user = User.query\
                    .filter(User.username == username).first()
                return user
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def get_by_id(id: int):
            try:
                user = User.query\
                    .filter(User.id == id).first()
                return user
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def delete_by_id(id: int):
            try:
                user = User.query\
                    .filter(User.id == id).delete()
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}' 
            
        @staticmethod
        def change_by_id(id: int, username: str = None, password: str = None, first_name: str = None, 
                 second_name: str = None, email: str = None, phone: str = None):
            try:
                user = User.query\
                    .filter(User.id== id).first()
                if username: user.username = username
                if password: user.password = password
                if email: user.email = email
                if phone: user.phone = phone
                if first_name: user.first_name = first_name
                if second_name: user.second_name = second_name
                db.session.commit()
                return user
            except Exception as e:
                return f'Произошла ошибка:\n{e}'  
            
        @staticmethod
        def change_by_username(username_first: str, username: str = None, password: str = None, first_name: str = None, 
                 second_name: str = None, email: str = None, phone: str = None):
            try:
                user = User.query\
                    .filter(User.username== username_first).first()
                if username: user.username = username
                if password: user.password = password
                if email: user.email = email
                if phone: user.phone = phone
                if first_name: user.first_name = first_name
                if second_name: user.second_name = second_name
                db.session.commit()
                return user
            except Exception as e:
                return f'Произошла ошибка:\n{e}'  
                   
    class bd_cart_product:
        pass
    class bd_favorite_product:
        pass
    class bd_comment:
        pass

class admin(user):
    class bd_category:
        pass
    class bd_second_category:
        pass
    class bd_third_category:
        pass
    class bd_product:
        pass
if __name__ == "__main__":
    
    with app.app_context():
        pass
        print(admin.bd_user.change_by_id(id=4, email='XXX@gmail'))
