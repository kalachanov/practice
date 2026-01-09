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
        
        @staticmethod
        def add_product(user_id: int, product_id: int):
            try:
                cart = CartProduct(user_id, product_id)
                db.session.add(cart)
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def delete_by_id(id: int):
            try:
                cart = CartProduct.query\
                    .filter(CartProduct.id == id).delete()
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def get_by_id(id: int):
            try:
                cart = CartProduct.query\
                    .filter(CartProduct.id == id).first()
                return cart
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def quantity_plus_by_id(id: int):
            try:
                cart = CartProduct.query\
                    .filter(CartProduct.id == id).first()
                cart.quantity = cart.quantity+1
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def quantity_minus_by_id(id: int):
            try:
                cart = CartProduct.query\
                    .filter(CartProduct.id == id).first()
                if cart.quantity==1:
                    cart = CartProduct.query\
                    .filter(CartProduct.id == id).delete()
                    db.session.commit()
                    return True
                else:
                    cart.quantity = cart.quantity-1
                    db.session.commit()
                    return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def quantity_change(id: int, number: int):
            try:
                cart = CartProduct.query\
                    .filter(CartProduct.id == id).first()
                if number <= 0:
                    return False
                else:
                    cart.quantity = number
                    db.session.commit()
                    return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
            
    class bd_favorite_product:
        
        @staticmethod
        def add_product(user_id: int, product_id: int):
            try:
                favorite = FavoriteProduct(user_id, product_id)
                db.session.add(favorite)
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def delete_by_id(id: int):
            try:
                favorite = FavoriteProduct.query\
                    .filter(FavoriteProduct.id == id).delete()
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def get_by_id(id: int):
            try:
                favorite = FavoriteProduct.query\
                    .filter(FavoriteProduct.id == id).first()
                return favorite
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
            
    class bd_comment:
        
        @staticmethod
        def add_comment(user_id: int, product_id: int, text: str):
            try:
                comment = Comment(user_id, product_id, text)
                db.session.add(comment)
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def delete_by_id(id: int):
            try:
                comment = Comment.query\
                    .filter(Comment.id == id).delete()
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def get_by_id(id: int):
            try:
                comment = Comment.query\
                    .filter(Comment.id == id).first()
                return comment
            except Exception as e:
                return f'Произошла ошибка:\n{e}'


class admin(user):

    class bd_category:
        
        @staticmethod
        def add_category(name: str, text: str):
            try:
                category = Category(name, text)
                db.session.add(category)
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def delete_by_id(id: int):
            try:
                category = Category.query\
                    .filter(Category.id == id).delete()
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def get_by_id(id: int):
            try:
                category = Category.query\
                    .filter(Category.id == id).first()
                return category
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def change_by_id(id: int, name: str = None, text: str = None):
            try:
                category = Category.query\
                    .filter(Category.id == id).first()
                if name: category.name = name
                if text: category.description = text
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
            
    class bd_second_category:
        @staticmethod
        def add_category(name: str, text: str, id: int):
            try:
                category = SecondCategory(name, text, id)
                db.session.add(category)
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def delete_by_id(id: int):
            try:
                category = SecondCategory.query\
                    .filter(SecondCategory.id == id).delete()
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def get_by_id(id: int):
            try:
                category = SecondCategory.query\
                    .filter(SecondCategory.id == id).first()
                return category
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def change_by_id(id: int, name: str = None, text: str = None, category_id: int = None):
            try:
                category = SecondCategory.query\
                    .filter(SecondCategory.id == id).first()
                if name: category.name = name
                if text: category.description = text
                if category_id: category.category_id = category_id
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
            
    class bd_third_category:
        
        @staticmethod
        def add_category(name: str, text: str, id: int):
            try:
                category = ThirdCategory(name, text, id)
                db.session.add(category)
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def delete_by_id(id: int):
            try:
                category = ThirdCategory.query\
                    .filter(ThirdCategory.id == id).delete()
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def get_by_id(id: int):
            try:
                category = ThirdCategory.query\
                    .filter(ThirdCategory.id == id).first()
                return category
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
        @staticmethod
        def change_by_id(id: int, name: str = None, text: str = None, category_id: int = None):
            try:
                category = ThirdCategory.query\
                    .filter(ThirdCategory.id == id).first()
                if name: category.name = name
                if text: category.description = text
                if category_id: category.category_id = category_id
                db.session.commit()
                return True
            except Exception as e:
                return f'Произошла ошибка:\n{e}'
            
            
    class bd_product:
        pass
    
    
    
if __name__ == "__main__":
    
    with app.app_context():
        pass
        print(admin.bd_cart_product.quantity_change(1, 0))
