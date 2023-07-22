from flask import Blueprint, request
from init import db, bcrypt
from models.pilot import Pilot, pilot_schema, pilots_schema
# from schemas.pilot_schema import pilot_schema, pilots_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes
from datetime import timedelta

pilots_bp = Blueprint('pilot', __name__, url_prefix='/pilots')

@pilots_bp.route('/')
def get_all_pilots():
    stmt = db.select(Pilot).order_by(Pilot.id)
    pilots = db.session.scalars(stmt)
    return pilots_schema.dump(pilots)

@pilots_bp.route('/register', methods=['POST'])
def pilot_register():
    try:
        # { "name": "___", "email": "___", "password": "___" }
        body_data = request.get_json()

        # Create a new pilot model instance from the user info
        pilot = Pilot() # Instance of the Pilot class which is in turn a SQLAlchemy model 
        pilot.arn = body_data.get('arn')
        pilot.name = body_data.get('name')
        pilot.email = body_data.get('email')
        if body_data.get('password'):
            pilot.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        # Add the pilot to the session
        db.session.add(pilot)
        # Commit to add the pilot to the database
        db.session.commit()
        # Respond to the client
        return pilot_schema.dump(pilot), 201
    except (DataError, IntegrityError) as err:
        if hasattr(err, 'orig') and hasattr(err.orig, 'pgcode'):
            if err.orig.pgcode == errorcodes.INVALID_TEXT_REPRESENTATION:
                return { 'Error': 'Come on Captain, you know arns are numbers only' }, 406
            elif err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return { 'Error': 'Sorry, either that arn or email address is already in use. Please try again.' }, 409
            elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return { 'Error': f'Oops, your {err.orig.diag.column_name} is required!' }, 409
        else:
            return { 'Error': 'Oh no, an unexpected database error occurred!' }, 500


@pilots_bp.route('/login', methods=['POST'])
def pilot_login():
    body_data = request.get_json()
    # Find the pilot by email
    stmt = db.select(Pilot).filter_by(email=body_data.get('email'))
    pilot = db.session.scalar(stmt)
    # If pilot exists and password is correct
    if pilot and bcrypt.check_password_hash(pilot.password, body_data.get('password')):
        token = create_access_token(identity=str(pilot.id), expires_delta=timedelta(days=1))
        return { 'email': pilot.email, 'token': token, 'is_admin': pilot.is_admin }
    else:
        return { 'Error': 'Oops, your email or password was incorrect. Please try again.' }, 418