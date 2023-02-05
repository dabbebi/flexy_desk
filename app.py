from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from sqlalchemy_utils import create_database, database_exists

# Create Flask application
app = Flask(__name__, static_folder='frontend/static')

# ORM instance
db = SQLAlchemy()

# marshmallow instance
ma = Marshmallow()

#config headers
CORS(app)

@app.route("/")
def welcome():
    return "<h2 style='text-align: center;'>back-end is running...</h2>"

# Static folder
@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("backend", 'static/' + path)

def init_database(flask_app, database, marshmallow, isSQLite = False):

    with flask_app.app_context():

        # Initialize database
        database.init_app(flask_app) 

        if not database_exists(flask_app.config["SQLALCHEMY_DATABASE_URI"]) and not isSQLite:
            create_database(flask_app.config["SQLALCHEMY_DATABASE_URI"])
            
        # Create sql tables for our data models
        database.create_all()
        
        # Initialize marshmallow
        marshmallow.init_app(flask_app)

def register_blueprints(flask_app):
    with flask_app.app_context():

        # Import parts of our application
        from backend.user.user_controller import user_bp  # Import user blueprint
        from backend.authentication.auth_controller import auth_bp # Import authentication blueprint
        from backend.place.place_controller import place_bp # Import place blueprint


        # Register Blueprints
        flask_app.register_blueprint(user_bp) # Register user blueprint
        flask_app.register_blueprint(auth_bp) # Register authentication blueprint
        flask_app.register_blueprint(place_bp) # Register place blueprint
    