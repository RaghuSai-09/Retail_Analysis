from flask import Flask
from flask_pymongo import PyMongo
import os 
from dotenv import load_dotenv

load_dotenv()
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.secret_key = 's3cret'
    app.config['MONGO_URI'] = os.getenv('MONGO_URL')
    mongo.init_app(app)
    
    # Register core blueprint
    from .routes import main
    app.register_blueprint(main)

    # Register modular blueprints
    from .chunk import churn_bp
    from .basket_analysis import basket_bp
    app.register_blueprint(churn_bp)
    app.register_blueprint(basket_bp)
    
    return app
