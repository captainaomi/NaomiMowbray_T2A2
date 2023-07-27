from init import ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


class FlightSchema(ma.Schema):
    # Include pilot's id and name from pilots table
    pilot = fields.Nested('PilotSchema', only=['id', 'name'])
    # Include aircraft id and callsign from aircraftz table
    aircraft_id = fields.Integer(required=True)

    # Validation for rest of flights fields:
    date = fields.Date(format='%Y-%m-%d', required=True)
    route = fields.String(required=True, validate=And(
        Length(
            min=10,
            max=100,
            error='Route should be between 10-100 characters long'
            ),
        Regexp(
            '^[a-zA-Z0-9.\-_. ]+$',
            error='Please only use letters, numbers, dashes or spaces'
            )
        )
    )
    flight_time = fields.Decimal(places=2, required=True)

    class Meta:
        fields = (
            'pilot',
            'aircraft_id',
            'aircraft_callsign',
            'id',
            'date',
            'route',
            'landings',
            'flight_time'
            )
        ordered = True

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)