from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ExampleProject.config import Config
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from ExampleProject.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	CORS(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	#Import all your blueprints
	from ExampleProject.main.routes import main
	from ExampleProject.users.routes import users
	from ExampleProject.errors.handlers import errors #ErrorHandler
	
	#use the url_prefix arguement if you need prefixes for the routes in the blueprint
	app.register_blueprint(main)
	app.register_blueprint(users, url_prefix='/users')
	app.register_blueprint(errors)

	return app

#Helper function to create database file directly from terminal
def create_database():
	import ExampleProject.models
	print("Creating App & Database")
	app = create_app()
	with app.app_context():
		db.create_all()
		db.session.commit()
	print("Successfully Created Database")