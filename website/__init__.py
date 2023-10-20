from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy() #defining database
DB_NAME = "databasePetMe.db"


def create_app(): 
    app = Flask(__name__) #initialising a flask application; __name__ is what we are running
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs' #securing the cookies and session data for our website
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #where database is located
    db.init_app(app) #initializing database by giving it a flask app

    from .views import views 
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') #registering the blueprints
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Ad, Image
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #where flask directs us if there"s no logged in user
    login_manager.init_app(app)

    @login_manager.user_loader #how we load a user
    def load_user(id):
        return User.query.get(int(id))

    
    return app

def create_database(app): #checks if database exists and if not, it creates it
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
