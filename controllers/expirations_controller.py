from flask import Blueprint, request
from init import db
from models.expirations import Expirations
from models.pilot import Pilot
from schemas.expirations_schema import expirations_schema, expirationsz_schema
from functions.admin_auth import admin_authorisation
from sqlalchemy.exc import DataError, IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import jwt_required


expirations_bp = Blueprint('expirations', __name__, url_prefix='/expirations')


# GET method to view all expiration entries in database
@expirations_bp.route('/')
def all_pilot_expirations():
    stmt = db.select(Expirations)
    pilot_expirations = db.session.scalars(stmt)
    return expirationsz_schema.dump(pilot_expirations), 200

# GET method to view an individual pilot's expirations entry
# in the database, using the pilot's id
@expirations_bp.route('/pilot/<int:pilot_id>')
def single_pilot_expirations(pilot_id):
    # Check if the pilot_id given in the route 
    # is an existing pilot with expirations
    stmt = db.select(Expirations).filter_by(pilot_id=pilot_id) 
    pilot_expirations = db.session.scalar(stmt)
    try:
        # If there's a pilot that matches the id with expirations, 
        # return their expiration dates
        if pilot_expirations:
            return expirations_schema.dump(pilot_expirations), 200
        # If there's not, give an error:
        else:
            return {
                'Error': f'Please check the pilot id; '
                'either they do not exist or have no expirations yet'}, 404
        
    # And because this might happen:
    except AttributeError:
        return {'Error': 'Are you sure that is a valid pilot id?' }, 404  
    # Catch any other random sneaky errors that might pop up in future
    except:
        return {
            'Error': 'Oh no, some weird error happened!' }, 500    


# POST method to create an expirations entry for a pilot 
# using the pilot's id (Note: only one entry per pilot)
@expirations_bp.route('/pilot/<int:pilot_id>', methods=['POST'])
# Check admin login, as this is an admin only method
@jwt_required()
@admin_authorisation
def add_expirations(pilot_id):
    # Load given expirations data from the request
    expirations_data = request.get_json()
    # Check if the pilot_id given in the route is an existing pilot
    stmt = db.select(Pilot).filter_by(id=pilot_id)
    pilot = db.session.scalar(stmt)
    #If there's no pilot that matches the pilot_id, give error
    if not pilot:
        return { 'Error': 'Dang, no pilot with that id was found' }, 404

    try:
        # Create a new expirations entry from the given data
        expirations = Expirations(
            pilot_id = pilot.id,
            medical = expirations_data.get('medical'),
            biannual_review = expirations_data.get(
                'biannual_review'),
            company_review = expirations_data.get(
                'company_review'),
            dangerous_goods = expirations_data.get(
                'dangerous_goods'),
            asic = expirations_data.get('asic'),
            pilot = pilot
        )
        # Add the new expirations to the session
        db.session.add(expirations)
        # Commit to add the new expirations to the database
        db.session.commit()
        # Nice job! Return the pilot's added expirations!
        return expirations_schema.dump(expirations), 201
    
    # For errors, give the following applicable messages:
    except (DataError, IntegrityError) as err:
        if hasattr(err, 'orig') and hasattr(err.orig, 'pgcode'):
            if err.orig.pgcode == errorcodes.INVALID_DATETIME_FORMAT:
                return {
                    'Error': 'That date looks funny; it should be YYYY-MM-DD'
                    }, 406
            elif err.orig.pgcode == errorcodes.DATETIME_FIELD_OVERFLOW:
                return {
                    'Error': 'Umm, are you sure that is a real date..?'
                    }, 406            
            elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {
                     'Error': f'{err.orig.diag.column_name} is missing' 
                     }, 406
            elif err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {
                    'Error': f'Pilot {pilot_id} already has expirations info; '
                    'please edit instead if they need updating'
                    }, 409
        else:
            return {
                'Error': 'Oh no, some weird error happened!' }, 500    
    except AttributeError:
        return {'Error': 'You need to login, silly!' }, 400  
    # Catch any other random sneaky errors that might pop up in future
    except:
        return { 'Error': 'Oh no, a mystery error occurred!' }, 500


# DELETE method to delete an expirations entry, using the id from route
@expirations_bp.route('/pilot/<int:pilot_id>', methods=['DELETE'])
# Check admin login, as this is an admin only method
@jwt_required()
@admin_authorisation
def delete_expirations(pilot_id):
    stmt = db.select(Expirations).filter_by(pilot_id=pilot_id)
    pilot_expirations = db.session.scalar(stmt)
    
    try:
        # If id in the route gives a vaild pilot, delete pilot  
        if pilot_expirations:
            db.session.delete(pilot_expirations)
            # Commit the deletion to the database
            db.session.commit()
            return {
                'Confirmation': 
                f'All done; expirations for pilot {pilot_id} were deleted!'
                }, 200
        else:
            return {
                'Error': f"Please check the pilot id; they either don't "
                "exist, or their expirations haven't been entered in yet"
                }, 404
        
    # Catch any other random sneaky errors that might pop up in future
    except:
        return { 'Error': 'Oh no, a mystery error occurred!' }, 500


# PUT and/or PATCH method to update or edit a pilot's expirations,
# using their pilot id in route
@expirations_bp.route('/pilot/<int:pilot_id>', methods=['PUT', 'PATCH'])
# Check admin login, as this is an admin only method
@jwt_required()
@admin_authorisation
def update_expirations(pilot_id):
    expirations_data = expirations_schema.load(request.get_json(), partial=True)
    stmt = db.select(Expirations).filter_by(pilot_id=pilot_id)
    pilot_expirations = db.session.scalar(stmt)

    try:
        # If id in the route gives a vaild pilot id, edit whatever  
        # information is given in JSON data
        if pilot_expirations:
            pilot_expirations.medical = expirations_data.get(
                'medical') or pilot_expirations.medical
            pilot_expirations.biannual_review = expirations_data.get(
                'biannual_review') or pilot_expirations.biannual_review
            pilot_expirations.company_review = expirations_data.get(
                'company_review') or pilot_expirations.company_review
            pilot_expirations.dangerous_goods = expirations_data.get(
                'dangerous_goods') or pilot_expirations.dangerous_goods
            pilot_expirations.asic = expirations_data.get(
                'asic') or pilot_expirations.asic
            # Commit the updated information to the database
            db.session.commit()
            return expirations_schema.dump(pilot_expirations), 201
        # If no pilot was found with that given id, or they don't 
        # have any expiration entry, give error:
        else:
            return {
                'Error': f"Please check the pilot id; they either don't "
                "exist, or their expirations haven't been entered in yet"
                }, 404
        
    # For other errors, give the following applicable messages:
    except (DataError, IntegrityError) as err:
        if hasattr(err, 'orig') and hasattr(err.orig, 'pgcode'):
            if err.orig.pgcode == errorcodes.INVALID_DATETIME_FORMAT:
                return {
                    'Error': 'That date looks funny; it should be YYYY-MM-DD'
                    }, 406
            elif err.orig.pgcode == errorcodes.DATETIME_FIELD_OVERFLOW:
                return {
                    'Error': 'Umm, are you sure that is a real date..?'
                    }, 406
        # Catch any other random sneaky errors that might pop up in future
        else:
            return {
                'Error': 'Oh no, some weird error happened!' }, 500    
    except:
        return {
            'Error': 'Oh no, some weird error happened!' }, 500    