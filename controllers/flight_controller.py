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


# This route is initially registered under aircraft_bp, 
# so it's actual route will be /aircraft/aircraft_id/expirations
flights_bp = Blueprint('flights', __name__, url_prefix='<int:aircraft_id>/flights')

@flights_bp.route('/')
def get_all_flights():
    stmt = db.select(Flight).order_by(Flight.id)
    all_flights = db.session.scalars(stmt)
    return flights_schema.dump(all_flights)


@flights_bp.route('/', methods=['POST'])
@jwt_required
def add_flight(aircraft_id): # seems to be an issue here?
    # Load given flight data from the request
    flight_data = flight_schema.load(request.get_json())
    stmt = db.select(Aircraft).filter_by(id=aircraft_id)
    aircraft = db.session.scalar(stmt)
    
    #If there's no aircraft that matches the aircraft_id
    if not aircraft:
        return { 'Error': f'Oops, no aircraft with id {aircraft_id} was found' }, 404

    try:
        # Create a new flight model from the given data
        new_flight = Flight()
        new_flight.pilot = get_jwt_identity()
        new_flight.aircraft = aircraft # how to get the aircraft id properly?? cant rememberrrr
        new_flight.date = flight_data.get('date')
        new_flight.route = flight_data.get('route')
        new_flight.landings = flight_data.get('landings')
        new_flight.flight_time = flight_data.get('flight_time')
            
        # Add the new pilot to the session
        db.session.add(new_flight)
        # Commit to add the new pilot to the database
        db.session.commit()

    # For errors, give the fowllowing applicable messages:
    except (KeyError, DataError, IntegrityError) as err:
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
                     'Error': f'{err.orig.diag.column_name} is missing' 
                     }, 406
        else:
            return { 'Error': 'Oh no, a mystery error occurred!' }, 500

