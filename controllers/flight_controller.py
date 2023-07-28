from flask import Blueprint, request
from init import db
from models.flight import Flight
from models.pilot import Pilot
from models.aircraft import Aircraft
from schemas.flight_schema import flight_schema, flights_schema
from functions.admin_auth import admin_authorisation
from sqlalchemy.exc import DataError, IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import jwt_required, get_jwt_identity


flight_bp = Blueprint('flight', __name__, url_prefix='/flight')


# GET method to view all flights in database
@flight_bp.route('/all_flights')
def get_all_flights():
    stmt = db.select(Flight).order_by(Flight.id)
    all_flights = db.session.scalars(stmt).all()
    if all_flights:
        return flights_schema.dump(all_flights), 200
    else:
        return {
            'Error': 
            f"There aren't any logged flights yet, so get up there!"}, 404


# GET method to view all flights for a specific aircraft, 
# using the aircraft id
@flight_bp.route('/aircraft/<int:aircraft_id>')
def aircraft_specific_flights(aircraft_id):
    # Check if the flight_id given in the route is correct
    stmt = db.select(Flight).filter_by(aircraft_id=aircraft_id)
    aircraft_flights = db.session.scalars(stmt).all()
    
    # If there are any flights that match the aircarft id, give those flights
    if aircraft_flights:
        return flights_schema.dump(aircraft_flights), 200
    # If there's no flight that matches the aircraft id, give an error instead
    else:
        return {
            'Error': 
            f"Aircraft {aircraft_id} is either invalid, inactive, " 
            "or hasn't completed any flights yet"}, 404


# GET method to view all flights for a specific pilot, 
# using the pilot's id
@flight_bp.route('/pilot/<int:pilot_id>')
def pilot_specific_flights(pilot_id):
    # Check if the flight_id given in the route is correct
    stmt = db.select(Flight).filter_by(pilot_id=pilot_id) 
    pilot_flights = db.session.scalars(stmt).all()
    # If there are no flights that match the pilot's id, give this error:
    if not pilot_flights:
        return {
            'Error': 
            f"Looks like pilot {pilot_id} hasn't completed any "
            "flights yet, they're inactive, or that's not a valid id."
            }, 404
    # If there are any flights that DO match the id, give those flights:
    elif pilot_flights:
        return flights_schema.dump(pilot_flights), 200
    # And just in case:
    else:
        return {
            'Error': f'{pilot_id} is not a valid pilot id, soz Captain!'}, 404
    

# GET method to view a single flight in database, using the flight id
@flight_bp.route('/<int:id>')
def get_one_flight(id):
    # Check if the flight_id given in the route is correct
    stmt = db.select(Flight).filter_by(id=id) 
    flight = db.session.scalar(stmt)
    # If there's a flight that matches the id, give that flight
    if flight:
        return flight_schema.dump(flight), 200
    # If there's no flight that matches the id, give an error instead
    else:
        return {
            'Error': f'{id} is not a valid flight id, soz Captain!'}, 404
    

# POST method to create a new flight
@flight_bp.route('/', methods=['POST'])
# Check the pilot is logged in correctly
@jwt_required()
def add_flight():
    # Get the authenticated pilot's identity for the flight,
    # as pilots can only create their own flights
    pilot_id = get_jwt_identity()
    # Fetch the Pilot object corresponding to the pilot_id
    pilot = Pilot.query.get(pilot_id)
    # Just in case it's an invalid login and they still snuck their way in:
    if not pilot:
        return {
            'Error': 'Cheeeeeeky! Not sure how you got here, '
            "as that's an invalid id!"}, 403
    # Load given flight data from the request
    flight_data = flight_schema.load(request.get_json())
    # Ensure aircraft_id is an integer to search through Aircraft objects
    aircraft_id = int(flight_data.get('aircraft_id'))
    # If the id is an integer, continue through code
    if aircraft_id:
        # Search for corresponding aircraft with that id
        aircraft = Aircraft.query.get(aircraft_id)
        # If aircraft is inactive, it can't be flown so throw error:
        if aircraft.status == 'inactive':
            return {
                'Error':
                "That aircraft can't take off; it's inactive!"
            }, 406
        #If there's no aircraft that matches the aircraft_id, give below error
        if not aircraft:
            return {
                'Error': 'Uh-oh, no aircraft with that id exists'
                }, 404
    #If aircraft_id is missing or not an integer, give below error
    else: 
        return {
            'Error': 'Uh-oh, you seems to be missing an aircraft id'
            }, 404
    
    # The aircraft is valid and active, so try to create a new flight:
    try:
        # Create a new flight model from the given data
        new_flight = Flight(
            pilot = pilot,
            aircraft = aircraft,
            date = flight_data.get('date'),
            route = flight_data.get('route'),
            landings = flight_data.get('landings'),
            flight_time = flight_data.get('flight_time')
            )
        # Add the new flight to the session
        db.session.add(new_flight)
        # Commit to add the new flight to the database
        db.session.commit()
        # Ensure the callsign, pilot's data and flight_id are included 
        # in the returned JSON data
        flight_data['aircraft_callsign'] = aircraft.callsign
        flight_data['pilot'] = {
            'id': pilot.id,
            'name': pilot.name
        }
        flight_data['id'] = new_flight.id
        # We did it! Return the new flight!
        return flight_schema.dump(flight_data), 201
    
    # For errors, have the following applicable messages ready to roll:
    except (DataError, IntegrityError) as err:
        if hasattr(err, 'orig') and hasattr(err.orig, 'pgcode'):
            if err.orig.pgcode == errorcodes.INVALID_TEXT_REPRESENTATION:
                return {
                    'Error': 'Use numbers for landings and flight time!'
                    }, 406
            elif err.orig.pgcode == errorcodes.INVALID_DATETIME_FORMAT:
                return {
                    'Error': 'That date looks funny; it should be YYYY-MM-DD'
                    }, 406
            elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {
                     'Error': f'Oops, {err.orig.diag.column_name} is missing' 
                     }, 406
        else:
            return { 'Error': 'Oh no, a mystery error occurred!' }, 500
    # Catch any other sneaky errors that might pop up in future
    except:
        return { 'Error': 'Oh no, a mystery error occurred!' }, 500
        

# DELETE method to delete a flight, using flight_id from route
@flight_bp.route('/<int:id>', methods=['DELETE'])
# Check admin login, as this is an admin only method
@jwt_required()
@admin_authorisation
def delete_aircraft(id):
    # Check if the flight_id given in the route is correct
    stmt = db.select(Flight).filter_by(id=id)
    flight = db.session.scalar(stmt)

    try:
        # If id in the route gives a vaild flight, delete flight  
        if flight:
            db.session.delete(flight)
            db.session.commit()
            return {'Confirmation': f'Flight {id} deleted successfully'}, 200
        # If the aircraft wasn't found, give error
        else:
            return {'Error': f'Uh-oh, no flight found with id {id}'}, 404
 
    # Catch any other sneaky errors that might pop up in future
    except:
        return { 'Error': 'Oh no, a mystery error occurred!' }, 500






# PUT and/or PATCH method to edit a flight,
# using the flight's id from route
@flight_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
# Check the pilot is logged in correctly
@jwt_required()
def update_flight(id):
    # Get the authenticated pilot's identity for the flight,
    # as pilots can only edit their own flights
    pilot_id = get_jwt_identity()
    # Fetch the Pilot object corresponding to the pilot_id
    pilot = Pilot.query.get(pilot_id)
    # Just in case it's an invalid login and they still snuck their way in:
    if not pilot:
        return {
            "Error': 'Cheeeeeeky! This either isn't your flight to edit "
            "or it's an invalid id; either way, no can do Captain"}, 403
    # Load given flight data from the request
    flight_data = flight_schema.load(request.get_json(), partial=True)
    # Check if the flight_id given in the route is correct
    stmt = db.select(Flight).filter_by(id=id)
    flight = db.session.scalar(stmt)

######### THIS IS WHAT I NEED TO CHECK NOW????? ########################################################
    # Ensure aircraft_id is an integer to search through Aircraft objects
    aircraft_id = int(flight_data.get('aircraft_id'))
    # If the id is an integer, continue through code
    if aircraft_id:
        # Search for corresponding aircraft with that id
        aircraft = Aircraft.query.get(aircraft_id)
        # If aircraft is inactive, it can't be flown so throw error:
        if aircraft.status == 'inactive':
            return {
                'Error':
                "That aircraft can't take off; it's inactive!"
            }, 406
        #If there's no aircraft that matches the aircraft_id, give below error
        if not aircraft:
            return {
                'Error': 'Uh-oh, no aircraft with that id exists'
                }, 404
    #If aircraft_id is missing or not an integer, give below error
    else: 
        return {
            'Error': 'Uh-oh, you seems to be missing an aircraft id'
            }, 404

    try:
        # If id in the route gives a vaild flight, edit whatever  
        # information is given in JSON data
        if flight:
            pilot = pilot,
            aircraft = flight_data.get('aircraft_id') or aircraft
            flight.date = flight_data.get('date') or flight.date
            flight.date = flight_data.get('date') or flight.date
            flight.date = flight_data.get('date') or flight.date
            flight.route = flight_data.get('route') or flight.route
            flight.landings = flight_data.get('landings') or flight.landings
            flight.flight_time = flight_data.get('flight_time') or flight.flight_time
            # Commit the updated information to the database
            db.session.commit()
            # Ensure the aircraft's callsign is included in the returned JSON data
            flight_data['aircraft_callsign'] = aircraft.callsign
            return flight_schema.dump(flight), 201
        # If the flight wasn't found, give error
        else:
            return {'Error': f'Uh-oh, no flight found with id {id}'}, 404
    
    # For errors, have the following applicable messages ready to roll:
    except (DataError, IntegrityError) as err:
        if hasattr(err, 'orig') and hasattr(err.orig, 'pgcode'):
            if err.orig.pgcode == errorcodes.INVALID_TEXT_REPRESENTATION:
                return {
                    'Error': 'Use numbers for landings and flight time!'
                    }, 406
            elif err.orig.pgcode == errorcodes.INVALID_DATETIME_FORMAT:
                return {
                    'Error': 'That date looks funny; it should be YYYY-MM-DD'
                    }, 406
        else:
            return { 'Error': 'Oh no, a mystery error occurred!' }, 500
    # Catch any other sneaky errors that might pop up in future
    except:
        return { 'Error': 'Oh no, a mystery error occurred!' }, 500
