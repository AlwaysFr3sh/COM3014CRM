# from flask import Flask
# # from flask_mongoengine import MongoClient
# from pymongo import MongoClient
# from flask_login import LoginManager
# # from utils import get_ssap
# # from .views import views
# # from api.auth import auth
# # from services.model import User, Company



# def create_app():
#     global db

#     app = Flask(__name__)
   
#     # MongoDB configuration
    
#     # mongodb_password=get_ssap("ssap.text")
#     # db_host=f"mongodb+srv://mnakhil:{mongodb_password}@crm.wjgi6mx.mongodb.net/?retryWrites=true&w=majority"
#     db_host=f"mongodb://localhost:27017/{db_name}"
#     app.config['MONGODB_HOST'] = db_host

#     # Initialize PyMongo
#     db = MongoClient()
#     db.init_app(app)

#     # Register blueprints
#     # app.register_blueprint(views, url_prefix='/')
#     print(init)

#     # Initialize login manager
#     # login_manager = LoginManager()
#     # login_manager.login_view = 'auth.login'
#     # login_manager.init_app(app)

#     # @login_manager.user_loader
#     # def load_user(id):
#     #     return User.objects.get(id=id)

#     return app