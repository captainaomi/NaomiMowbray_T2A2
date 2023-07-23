from flask import Blueprint, jsonify, request
from init import db, bcrypt
from models.pilot import Pilot
from schemas.pilot_schema import pilot_schema, pilots_schema
from controllers.expirations_controller import expirations_bp
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes
from datetime import timedelta


pilots_bp = Blueprint('pilot', __name__, url_prefix='/pilots')
pilots_bp.register_blueprint(expirations_bp)


@pilots_bp.route('/')
def get_all_pilots():
    stmt = db.select(Pilot).order_by(Pilot.id)
    all_pilots = db.session.scalars(stmt)
    return pilots_schema.dump(all_pilots)

@pilots_bp.route('/register', methods=['POST'])
def register_pilot():
    # Load given pilot data from the request
    pilot_data = pilot_schema.load(request.get_json())

    try:
        # Create a new pilot model from the given data
        new_pilot = Pilot()
        new_pilot.arn = pilot_data.get('arn')
        new_pilot.name = pilot_data.get('name')
        new_pilot.email = pilot_data.get('email')
        if pilot_data.get('password'):
            new_pilot.password = bcrypt.generate_password_hash(
                pilot_data.get('password')).decode('utf-8')
        new_pilot.status = pilot_data.get('status')
        new_pilot.is_admin = pilot_data.get('is_admin')
        # Add the new pilot to the session
        db.session.add(new_pilot)
        # Commit to add the new pilot to the database
        db.session.commit()

        # Serialize the new pilot using the schema 
        # without the password field, by using pop
        serialized_pilot = pilot_schema.dump(new_pilot)
        serialized_pilot.pop('password')
        
        # Congrats! Return the new pilot!
        return jsonify(serialized_pilot), 201
    
    # For errors, give the fowllowing applicable messages:
    except (KeyError, DataError, IntegrityError) as err:
        if hasattr(err, 'orig') and hasattr(err.orig, 'pgcode'):
            if err.orig.pgcode == errorcodes.INVALID_TEXT_REPRESENTATION:
                return { 'Error': 'Oops, arns are numbers only!' }, 418
            elif err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {
                     'Error': 'That arn or email is already in use.' 
                     }, 409
            elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {
                     'Error': f'{err.orig.diag.column_name} is missing' 
                     }, 406
        else:
            return { 'Error': 'Oh no, a mystery error occurred!' }, 500
        

@pilots_bp.route('/login', methods=['POST'])
def login_pilot():
    body_data = request.get_json()
    # Find the pilot by email
    stmt = db.select(Pilot).filter_by(email=body_data.get('email'))
    pilot = db.session.scalar(stmt)
    # If pilot exists and password is correct
    if pilot and bcrypt.check_password_hash(
        pilot.password, body_data.get('password')):
        token = create_access_token(
            identity=str(pilot.id), expires_delta=timedelta(days=1))
        return {
             'email': pilot.email,
             'token': token,
             'is_admin': pilot.is_admin
             }
    else:
        return {
            'Error': 'Looks like your email or password is incorrect'
            }, 418