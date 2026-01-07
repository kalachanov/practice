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
            
        # @staticmethod
        # def login(username: str, password: str, email: str = None, phone: str = None):
        #     try:
                
        #         return db.Query.select_from(User).filter(User.username == username and User.password == password)
        #     except Exception as e:
        #         return f'Произошла ошибка:\n{e}' 
                   
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
        # print(user.bd_user.login('Funf', '1234',))
