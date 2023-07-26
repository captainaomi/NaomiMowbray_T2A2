from flask import Blueprint, request
from init import db
from models.aircraft import Aircraft
from schemas.aircraft_schema import aircraft_schema, aircraftz_schema
from functions.admin_auth import admin_authorisation
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


aircraft_bp = Blueprint('aircraft', __name__, url_prefix='/aircraft')


# GET method to view all aircraft in database
@aircraft_bp.route('/')
def get_all_aircraft():
    stmt = db.select(Aircraft).order_by(Aircraft.id)
    all_aircraft = db.session.scalars(stmt)
    return aircraftz_schema.dump(all_aircraft)


# GET method to view a single aircraft in database, using the aircraft id
@aircraft_bp.route('/<int:id>')
def get_one_aircraft(id):
    # Check if the aircraft_id given in the route is correct
    stmt = db.select(Aircraft).filter_by(id=id) 
    aircraft = db.session.scalar(stmt)
    if aircraft:
        return aircraft_schema.dump(aircraft)
    else:
        return {
            'Error': f'There is no aircraft with id {id} (yet!)'}, 404
    

# POST method to create a new aircraft in the database
@aircraft_bp.route('/', methods=['POST'])
# Check user login, as this is an admin only method
@jwt_required()
@admin_authorisation

def add_aircraft():
    # Load given aircraft data from the request
    aircraft_data = aircraft_schema.load(request.get_json())
    
    # Check if an aircraft with the same callsign already exists
    existing_aircraft = Aircraft.query.filter_by(
        callsign=aircraft_data['callsign']).first()

# # # # # # # # # # DOES THIS NEED TO BE IN THE TRY BLOCK?????
    if existing_aircraft:
        return { 'Error': 'That aircraft already exists.' }, 409

    try:
        # Create a new aircraft model from the given data
        new_aircraft = Aircraft()
        new_aircraft.callsign = aircraft_data.get('callsign')
        new_aircraft.status = aircraft_data.get('status')

        # Add the new aircraft to the session
        db.session.add(new_aircraft)
        # Commit to add the new aircraft to the database
        db.session.commit()
        
        # Congrats! Return the shiny new aircraft!
        return aircraft_schema.dump(new_aircraft), 201
    
    except:
        return { 'Error': 'Oh no, an unexpected error occurred!' }, 500
    

# DELETE method to delete an aircraft, using the id from route
@aircraft_bp.route('/<int:id>', methods=['DELETE'])
# Check user login, as this is an admin only method
@jwt_required()
@admin_authorisation
def delete_aircraft(id):
    stmt = db.select(Aircraft).filter_by(id=id)
    aircraft = db.session.scalar(stmt)
    if aircraft:
        db.session.delete(aircraft)
        db.session.commit()
        return {'Confirmation': f'Aircraft {aircraft.callsign} deleted successfully'}, 201
    else:
        return {'Error': f'Uh-oh, no aircraft found with id {id}'}, 404
    
    
# PUT and/or PATCH method to update or edit an aircraft, using the id from route
@aircraft_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
# Check user login, as this is an admin only method
@jwt_required()
@admin_authorisation

def update_aircraft(id):
    aircraft_data = aircraft_schema.load(request.get_json(), partial=True)
    stmt = db.select(Aircraft).filter_by(id=id)
    aircraft = db.session.scalar(stmt)
    try:
        if aircraft:
            aircraft.callsign = aircraft_data.get('callsign') or aircraft.callsign
            aircraft.status = aircraft_data.get('status') or aircraft.status

            db.session.commit()
            return aircraft_schema.dump(aircraft), 201
        else:
            return {'Error': f'Uh-oh, no aircraft found with id {id}'}, 404
    except IntegrityError as err:
        if hasattr(err, 'orig') and hasattr(err.orig, 'pgcode'):
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {
                    'Error': 'No can do; that arn or email is already in use.' 
                    }, 409
        else:
            return { 'Error': 'Oh no, a mystery error occurred!' }, 500
