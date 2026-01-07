from config import CONFIG
from models import *
from flask import Flask

app = Flask(__name__)    
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

class user:
    class bd_user:
        pass
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


    



with app.app_context():
    pass