from flask import Blueprint, request
from init import db
from models.aircraft import Aircraft
from schemas.aircraft_schema import aircraft_schema, aircraftz_schema
from controllers.flight_controller import flights_bp
from functions.admin_auth import admin_authorisation
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError


aircraft_bp = Blueprint('aircraft', __name__, url_prefix='/aircraft')
aircraft_bp.register_blueprint(flights_bp)


@aircraft_bp.route('/')
def get_all_aircraft():
    stmt = db.select(Aircraft).order_by(Aircraft.id)
    all_aircraft = db.session.scalars(stmt)
    return aircraftz_schema.dump(all_aircraft)

@aircraft_bp.route('/', methods=['POST'])
def add_aircraft():
    # Load given aircraft data from the request
    aircraft_data = aircraft_schema.load(request.get_json())
    
    # Check if an aircraft with the same callsign already exists
    existing_aircraft = Aircraft.query.filter_by(
        callsign=aircraft_data['callsign']).first()

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
    
    except IntegrityError:
        db.session.rollback()
        return { 'Error': 'Oh no, an unexpected error occurred!' }, 500
    

@aircraft_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_authorisation
def delete_aircraft(id):
    stmt = db.select(Aircraft).filter_by(id=id)
    aircraft = db.session.scalar(stmt)
    if aircraft:
        db.session.delete(aircraft)
        db.session.commit()
        return {'Confirmation': f'Aircraft {aircraft.callsign} deleted successfully'}
    else:
        return {'Error': f'Uh-oh, no aircraft found with id {id}'}, 404
    
    
@aircraft_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@admin_authorisation
def update_aircraft(id):
    aircraft_data = aircraft_schema.load(request.get_json(), partial=True)
    stmt = db.select(Aircraft).filter_by(id=id)
    aircraft = db.session.scalar(stmt)
    if aircraft:
        aircraft.callsign = aircraft_data.get('callsign') or aircraft.callsign
        aircraft.status = aircraft_data.get('status') or aircraft.status

        db.session.commit()
        return aircraft_schema.dump(aircraft)
    else:
        return {'Error': f'Uh-oh, no aircraft found with id {id}'}, 404