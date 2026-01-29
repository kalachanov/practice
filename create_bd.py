from config import CONFIG
from models import *

if __name__ == "__main__":
    from flask import Flask
    
    app = Flask(__name__)    
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG.SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)
    # ! Cоздать отдельную функцию для создании БД
    with app.app_context():
        db.create_all()