from flask import Blueprint, jsonify, request
from init import db, bcrypt
from models.pilot import Pilot
from schemas.pilot_schema import pilot_schema, pilots_schema
from flask_jwt_extended import create_access_token
from functions.admin_auth import admin_authorisation
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes
from datetime import timedelta


pilots_bp = Blueprint('pilot', __name__, url_prefix='/pilots')


# GET method to view all pilots in database
@pilots_bp.route('/')
def get_all_pilots():
    stmt = db.select(Pilot).order_by(Pilot.id)
    all_pilots = db.session.scalars(stmt)
    return pilots_schema.dump(all_pilots), 200


# GET method to view a single pilot in database, using the pilot id
@pilots_bp.route('/<int:id>')
def get_one_pilot(id):
    # Check if the pilot_id given in the route is correct
    stmt = db.select(Pilot).filter_by(id=id) 
    pilot = db.session.scalar(stmt)
    # If there's a pilot that matches the id, return that pilot
    if pilot:
        return pilot_schema.dump(pilot), 200
    
    # If there's no pilot that matches the id, give an error instead
    else:
        return {
            'Error': f'{id} is not a valid pilot id, soz Captain!'}, 418


# POST method to register a new pilot
@pilots_bp.route('/register', methods=['POST'])
# Check user login, as this is an admin only method
@jwt_required()
@admin_authorisation
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
    
    # For errors, give the following applicable messages:
    except (KeyError, DataError, IntegrityError) as err:
        if hasattr(err, 'orig') and hasattr(err.orig, 'pgcode'):
            if err.orig.pgcode == errorcodes.INVALID_TEXT_REPRESENTATION:
                return { 'Error': 'Oops, arns are numbers only!' }, 418
            elif err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {
                     'Error': 
                     'Hold on, that arn or email is already in use...' 
                     }, 409
            elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {
                     'Error': 
                     f'Ahhhh, {err.orig.diag.column_name} is missing?' 
                     }, 406
        else:
            return { 'Error': 'Oh no, a mystery error occurred!' }, 500
        

# POST method to for a pilot to login 
@pilots_bp.route('/login', methods=['POST'])
def login_pilot():
    body_data = request.get_json()
    # Find the pilot by email
    stmt = db.select(Pilot).filter_by(email=body_data.get('email'))
    pilot = db.session.scalar(stmt)

    try:
        # Check if pilot exists and their status is NOT inactive, 
        # because if they're inactive, they can't login anymore!
        if pilot and pilot.status == 'inactive':
            return {
                'Error': 'This is awkward... Maybe talk to your Chief Pilot'
                ' as your account is inactive'
                }, 403
        
        # Now check if the email plus password combo is correct
        elif pilot and bcrypt.check_password_hash(
            pilot.password, body_data.get('password')):
            token = create_access_token(
                identity=str(pilot.id), expires_delta=timedelta(days=1))
            return {
                'email': pilot.email,
                'status': pilot.status,
                'token': token,
                'is_admin': pilot.is_admin
                }, 200
        
        # If either are incorrect, give error
        else:
            return {
                'Error': 'Looks like your email or password is incorrect'
                }, 418
    # Catch any other random sneaky errors that might pop up in future
    except:
        return { 'Error': 'Oh no, a mystery error occurred!' }, 500


# DELETE method to delete a pilot, using the id from route
@pilots_bp.route('/<int:id>', methods=['DELETE'])
# Check user login, as this is an admin only method
@jwt_required()
@admin_authorisation
def delete_pilot(id):
    stmt = db.select(Pilot).filter_by(id=id)
    pilot = db.session.scalar(stmt)

    try:
        if pilot:
            db.session.delete(pilot)
            db.session.commit()
            return {
                'Confirmation': 
                f'Captain {pilot.name} has been successfully deleted'
                }, 200
        else:
            return {'Error': f'Uh-oh, no pilot found with id {id}'}, 404
    # Catch any other random sneaky errors that might pop up in future
    except:
        return { 'Error': 'Oh no, a mystery error occurred!' }, 500

    
# PUT and/or PATCH method to update or edit a pilot, using the id from route
@pilots_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
# Check user login, as this is an admin only method
@jwt_required()
@admin_authorisation

def update_pilot(id):
    pilot_data = pilot_schema.load(request.get_json(), partial=True)
    stmt = db.select(Pilot).filter_by(id=id)
    pilot = db.session.scalar(stmt)

    try:
        if pilot:
            pilot.arn = pilot_data.get('arn') or pilot.arn
            pilot.name = pilot_data.get('name') or pilot.name
            pilot.email = pilot_data.get('email') or pilot.email
            pilot.status = pilot_data.get('status') or pilot.status
            pilot.is_admin = pilot_data.get('is_admin') or pilot.is_admin
            db.session.commit()
            # Serialize the new pilot using the schema 
            # without the password field, by using pop
            serialized_pilot = pilot_schema.dump(pilot)
            serialized_pilot.pop('password')
            
            # Congrats! Return the new pilot!
            return jsonify(serialized_pilot), 201
        else:
            return {'Error': f'Uh-oh, no pilot found with id {id}'}, 404
    # Catch any other random sneaky errors that might pop up in future
    except(KeyError, DataError, IntegrityError) as err:
        if hasattr(err, 'orig') and hasattr(err.orig, 'pgcode'):
            if err.orig.pgcode == errorcodes.INVALID_TEXT_REPRESENTATION:
                return { 'Error': 'Oops, arns are numbers only!' }, 418
            elif err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {
                     'Error': 'That arn or email is already in use.' 
                     }, 409
        else:
            return { 'Error': 'Oh no, a mystery error occurred!' }, 500
