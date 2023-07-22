from init import ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


class FlightSchema(ma.Schema):
    pilot = fields.Nested('PilotSchema', only=['id', 'arn', 'name'])
    aircraft = ('AircraftSchema',)

    route = fields.String(required=True, validate=And(
        Length(min=10, error='Route must be at least ten characters long'),
        Regexp('^[a-zA-Z0-9.\-_. ]+$', error='Please only use letters, numbers, dashes or spaces')
    ))

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