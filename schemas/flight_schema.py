from init import ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp
from marshmallow.exceptions import ValidationError


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
            '^[a-zA-Z0-9\.\-\ \!]+$',
            error='You can use letters, numbers, dashes, spaces, full stops - '
            'and a cheeky exclamation point if it was a great flight!'
            )
        )
    )
    landings = fields.Integer(coerce=int)
    flight_time = fields.Decimal(
        places=2,
        required=True
        )

    @validates('landings')
    def validate_landings(self, value):
        # Check for integer and coerce the values if given as string
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                    raise ValidationError(f"Come on, '{value}' for 'landings' is not a valid integer.")

    @validates('flight_time')
    def validate_flight_time(self, value):
        max_flight_time = 99.99
        if value > max_flight_time:
            raise ValidationError("Surely you didn't fly that long! Flight time "
            "is max. 99.98hrs (even though that's unlikely!)"
            )

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
    route = fields.String(required=True, validate=And(
        Length(
            min=10,
            max=100,
            error='Route should be between 10-100 characters long'
            ),
        Regexp(
            '^[a-zA-Z0-9\.\-\ \!]+$',
            error='You can use letters, numbers, dashes, spaces, full stops - '
            'and a cheeky exclamation point if it was a great flight!'
            )
        )
    )
    flight_time = fields.Decimal(
        places=2,
        required=True
        )
    landings = fields.Integer(coerce=int)
    flight_time = fields.Decimal(places=2)

    @validates('flight_time')
    def validate_flight_time(self, value):
        max_flight_time = 99.99
        if value > max_flight_time:
            raise ValidationError("Surely you didn't fly that long! Flight time "
            "is max. 99.98hrs (even though that's unlikely!)"
            )
        
    @validates('landings')
    def validate_landings(self, value):
        # Check for integer and coerce the values if given as string
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                    raise ValidationError(f"Come on, '{value}' for 'landings' is not a valid integer.")
                
flightpatch_schema = FlightPatchSchema()
