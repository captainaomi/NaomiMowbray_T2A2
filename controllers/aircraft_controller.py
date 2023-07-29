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
@aircraft_bp.route('/all_aircraft')
@jwt_required()
def get_all_aircraft():
    stmt = db.select(Aircraft).order_by(Aircraft.id)
    all_aircraft = db.session.scalars(stmt).all()
    if all_aircraft:
        return aircraftz_schema.dump(all_aircraft), 200
    else:
        return {
            'Error': 
            f"Oops, there aren't any aircraft in here yet!"}, 404

# GET method to view a single aircraft in database, using the aircraft id
@aircraft_bp.route('/<int:id>')
@jwt_required()
def get_one_aircraft(id):
    # Check if the aircraft_id given in the route is correct
    stmt = db.select(Aircraft).filter_by(id=id) 
    aircraft = db.session.scalar(stmt)
    
    # If there's an aircraft that matches the id, return that aircraft
    if aircraft:
        return aircraft_schema.dump(aircraft), 200
    # If there's no aircraft that matches the id, give an error instead
    else:
        return {
            'Error': f'There is no aircraft with id {id} (yet!)'}, 404
    

# POST method to create a new aircraft in the database
@aircraft_bp.route('/', methods=['POST'])
# Check admin login, as this is an admin only method
@jwt_required()
@admin_authorisation
def add_aircraft():
    # Load given aircraft data from the request
    aircraft_data = aircraft_schema.load(request.get_json())
    
    # Check if an aircraft with the same callsign already exists
    existing_aircraft = Aircraft.query.filter_by(
        callsign=aircraft_data['callsign']).first()
    # If it does exist already, give this error and stop there:
    if existing_aircraft:
        return { 'Error': 'That aircraft already exists.' }, 409
    
    # The aircraft callsign is new, so try to create a new aircraft:
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
    
    # Catch any other sneaky errors that might pop up in future
    except:
        return { 'Error': 'Oh no, an unexpected error occurred!' }, 500
    

# DELETE method to delete an aircraft, using the aircraft_id from route
@aircraft_bp.route('/<int:id>', methods=['DELETE'])
# Check user login, as this is an admin only method
@jwt_required()
@admin_authorisation
def delete_aircraft(id):
    # Check if the aircraft_id given in the route is correct
    stmt = db.select(Aircraft).filter_by(id=id)
    aircraft = db.session.scalar(stmt)

    try:
        # If id in the route gives a vaild aircraft, delete aircraft  
        if aircraft:
            db.session.delete(aircraft)
            # Commit the deletion to the database
            db.session.commit()
            return {
                'Confirmation': 
                f'Aircraft {aircraft.callsign} deleted successfully'
                }, 200
        # If the aircraft wasn't found, give error
        else:
            return {
                'Error': 
                f'Uh-oh, no aircraft found with id {id}'
                }, 404
        
    # Catch any other sneaky errors that might pop up in future
    except:
        return { 'Error': 'Oh no, a mystery error occurred!' }, 500
    

# PUT and/or PATCH method to update or edit an aircraft,
# using the aircraft's id from route
@aircraft_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
# Check user login, as this is an admin only method
@jwt_required()
@admin_authorisation
def update_aircraft(id):
    # Check if the aircraft_id given in the route is correct
    aircraft_data = aircraft_schema.load(request.get_json(), partial=True)
    stmt = db.select(Aircraft).filter_by(id=id)
    aircraft = db.session.scalar(stmt)

    try:
        # If id in the route gives a vaild aircraft, edit whatever  
        # information is given in JSON data
        if aircraft:
            aircraft.callsign = aircraft_data.get('callsign') or aircraft.callsign
            aircraft.status = aircraft_data.get('status') or aircraft.status
            # Commit the updated information to the database
            db.session.commit()
            return aircraft_schema.dump(aircraft), 201
        # If the aircraft wasn't found, give error
        else:
            return {'Error': f'Uh-oh, no aircraft found with id {id}'}, 404
    
    # If unique or other integrity error pops up, give messages:
    except IntegrityError as err:
        if hasattr(err, 'orig') and hasattr(err.orig, 'pgcode'):
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {
                    'Error': 'No can do; that arn or email is already in use.' 
                    }, 409
        else:
            return { 'Error': 'Oh no, a mystery error occurred!' }, 500
    # Catch any other sneaky errors that might pop up in future
    except:
        return { 'Error': 'Oh no, an unexpected error occurred!' }, 500