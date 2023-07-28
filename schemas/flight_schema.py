from init import ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


class FlightSchema(ma.Schema):
    # Include pilot's id and name from pilot table
    pilot = fields.Nested('PilotSchema', only=['id', 'name'])
    # Include aircraft id from aircraft table
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
            'id',
            'date',
            'route',
            'landings',
            'flight_time'
            )
        ordered = True

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)


class FlightPatchSchema(ma.Schema):
    aircraft_id = fields.Integer()
    date = fields.Date(format='%Y-%m-%d')
    route = fields.String(validate=And(
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
    landings = fields.Integer()
    flight_time = fields.Decimal(places=2)

flightpatch_schema = FlightPatchSchema()
