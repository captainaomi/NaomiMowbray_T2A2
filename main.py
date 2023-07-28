from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.pilot_controller import pilot_bp
from controllers.aircraft_controller import aircraft_bp
from controllers.expirations_controller import expirations_bp
from controllers.flight_controller import flight_bp
from marshmallow.exceptions import ValidationError


def create_app(): 
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")


    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'Error': err.messages}, 400


    @app.errorhandler(400)
    def bad_request(err):
        return {'Error': str(err)}, 400
    
    
    @app.errorhandler(404)
    def not_found(err):
        return {'Error': str(err)}, 404

    @app.errorhandler(500)
    def server_error(err):
        return {'Error': str(err)}, 500

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)


    app.register_blueprint(db_commands)
    app.register_blueprint(pilot_bp)
    app.register_blueprint(aircraft_bp)
    app.register_blueprint(expirations_bp)
    app.register_blueprint(flight_bp)


    return app