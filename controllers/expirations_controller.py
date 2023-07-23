from flask import Blueprint, request
from init import db
from models.expirations import Expirations
from models.pilot import Pilot
from schemas.expirations_schema import expirations_schema, expirationsz_schema
from sqlalchemy.exc import DataError
from psycopg2 import errorcodes
from flask_jwt_extended import jwt_required, get_jwt_identity


# This route is initially registered under pilots_bp, 
# so it's actual route will be /pilots/pilot_id/expirations
expirations_bp = Blueprint(
    'expirations',__name__, url_prefix='/<int:pilot_id>/expirations'
    )


@expirations_bp.route('/')
def get_all_pilots():
    stmt = db.select(Expirations).order_by(Expirations.id)
    all_expirations = db.session.scalars(stmt)
    return expirationsz_schema.dump(all_expirations)

@expirations_bp.route('/', methods=['POST'])
@jwt_required()
def add_expirations(pilot_id):
    # Load given expirations data from the request
    expirations_data = request.get_json()
    stmt = db.select(Pilot).filter_by(id=pilot_id)
    pilot = db.session.scalar(stmt)
    
    #If there's a pilot that matches the pilot_id
    if not pilot:
        return { 'Error': 'Oops, that pilot was not found' }, 404

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
    
    except DataError as err:
        if hasattr(err, 'orig') and hasattr(err.orig, 'pgcode'):
            if err.orig.pgcode == errorcodes.INVALID_DATETIME_FORMAT:
                return {
                    'Error': 'That date looks funny; it should be YYYY-MM-DD'
                    }, 406
        else:
            return {
                'Error': 'Oh no, some weird error happened!' }, 500
        
    except TypeError:
        # Custom error message for TypeError
        return {'Error': 'A TypeError occurred; please check your data.'}, 400