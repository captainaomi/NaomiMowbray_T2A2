from flask import Blueprint, request
from init import db
from models.expirations import Expirations
from models.pilot import Pilot
from schemas.expirations_schema import expirations_schema, expirationsz_schema
from functions.admin_auth import admin_authorisation
from sqlalchemy.exc import DataError, IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import jwt_required, get_jwt_identity


expirations_bp = Blueprint('expirations',__name__, url_prefix='/expirations')


@expirations_bp.route('/')
def all_pilot_expirations():
    stmt = db.select(Expirations)
    pilot_expirations = db.session.scalars(stmt)
    return expirationsz_schema.dump(pilot_expirations)


@expirations_bp.route('/pilot/<int:pilot_id>')
def single_pilot_expirations(pilot_id):
    # Check if the pilot_id given in the route 
    # is an existing pilot with expirations
    stmt = db.select(Expirations).filter_by(pilot_id=pilot_id) 
    pilot_expirations = db.session.scalar(stmt)
    if pilot_expirations:
        return expirations_schema.dump(pilot_expirations)
    else:
        return {
            'Error': f'Please check the pilot id; '
            'either they do not exist or have no expirations yet'}, 404


@expirations_bp.route('/pilot/<int:pilot_id>', methods=['POST'])
@jwt_required()
@admin_authorisation
def add_expirations(pilot_id):
    # Load given expirations data from the request
    expirations_data = request.get_json()
    # Check if the pilot_id given in the route is an existing pilot
    stmt = db.select(Pilot).filter_by(id=pilot_id)
    pilot = db.session.scalar(stmt)
    
    #If there's no pilot that matches the pilot_id
    if not pilot:
        return { 'Error': f'Dang, no pilot with that id was found' }, 404

    try:
        # Create a new expirations model from the given data
        expirations = Expirations(
            pilot_id = get_jwt_identity(),
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
        
        # Congrats! Return the added pilot expirations!
        return expirations_schema.dump(expirations), 201
    
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
        else:
            return {
                'Error': 'Oh no, some weird error happened!' }, 500    


@expirations_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_authorisation
def delete_expirations(id):
    stmt = db.select(Expirations).filter_by(id=id)
    expirations = db.session.scalar(stmt)
    if expirations:
        db.session.delete(expirations)
        db.session.commit()
        return {'Confirmation': f'Expirations {expirations.pilot} deleted successfully'} # Not sure if pilot will work?
    else:
        return {'Error': f'Uh-oh, no expirations found with id {id}'}, 404


@expirations_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@admin_authorisation
def update_expirations(id):
    expirations_data = expirations_schema.load(request.get_json(), partial=True)
    stmt = db.select(Expirations).filter_by(id=id)
    expirations = db.session.scalar(stmt)
    if expirations:
        expirations.medical = expirations_data.get(
            'medical') or expirations.medical
        expirations.biannual_review = expirations_data.get(
            'biannual_review') or expirations.biannual_review
        expirations.company_review = expirations_data.get(
            'company_review') or expirations.company_review
        expirations.dangerous_goods = expirations_data.get(
            'dangerous_goods') or expirations.dangerous_goods
        expirations.asic = expirations_data.get(
            'asic') or expirations.asic

        db.session.commit()
        return expirations_schema.dump(expirations)
    else:
        return {'Error': f'Uh-oh, no expirations found with id {id}'}, 404