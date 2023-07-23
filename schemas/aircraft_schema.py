from init import ma
from marshmallow import fields
from marshmallow.validate import And, Length, Regexp, OneOf


VALID_STATUSES = ('active', 'inactive')


class AircraftSchema(ma.Schema):
    callsign = fields.String(required=True, validate=And(
        Length(
            max=10, 
            error='Callsigns are not that long! Max. 10 characters pls'
            ),
        Regexp(
            '^[A-Z0-9\-]+$',
            error='Please only use capital letters, numbers, or dashes'
            )
        )
    )
    status = fields.String(required=True, validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = ('id', 'callsign', 'status')
        ordered = True

aircraft_schema = AircraftSchema()
aircraftz_schema = AircraftSchema(many=True)