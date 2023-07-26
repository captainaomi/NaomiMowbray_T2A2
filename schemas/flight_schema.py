from init import db, ma
from models.aircraft import Aircraft
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp
from marshmallow.exceptions import ValidationError


class FlightSchema(ma.Schema):
    pilot = fields.Nested('PilotSchema', only=['id', 'name'])
    aircraft = fields.Nested('AircraftSchema', only=['callsign'], required=True)
    date = fields.DateTime(format='%Y-%m-%-d', required=True)
   
    @validates('aircraft_id')
    def validate_callsign(self, value):
            stmt = db.select(db.func.count()).select_from(Aircraft).filter_by(id=value)
            count=db.session.scalar(stmt)
            if count < 1 :
                raise ValidationError('Uh-oh, no aircraft with that id exists')

    route = fields.String(required=True, validate=And(
        Length(
            min=10,
            max=100,
            error='Route must between 10-100 characters long'
            ),
        Regexp(
            '^[a-zA-Z0-9.\-_. ]+$',
            error='Please only use letters, numbers, dashes or spaces'
            )
        )
    )

    class Meta:
        fields = (
            'pilot',
            'aircraft',
            'id',
            'date',
            'route',
            'landings',
            'flight_time'
            )
        ordered = True

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)


    # # Check if that aircraft exists
    # @validates('aircraft_id')
    # def validate_callsign(self, data):
    #         stmt = db.select(db.func.count()).select_from(Aircraft).filter_by(id=value)
    #         count=db.session.scalar(stmt)
    #         if count < 1 :
    #             raise ValidationError('Uh-oh, no aircraft with that id exists')

    # route = fields.String(required=True, validate=And(
    #     Length(
    #         min=10,
    #         max=100,
    #         error='Route must between 10-100 characters long'
    #         ),
    #     Regexp(
    #         '^[a-zA-Z0-9.\-_. ]+$',
    #         error='Please only use letters, numbers, dashes or spaces'
    #         )
    #     )
    # )