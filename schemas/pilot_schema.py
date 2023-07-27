from init import ma
from marshmallow import fields
from marshmallow.validate import Email, OneOf, And, Length, Regexp


VALID_STATUSES = ('active', 'inactive')


class PilotSchema(ma.Schema):

    # Validation for pilot fields:
    name = fields.String(
        required=True, 
        validate=And(
            Length(
                min=4,
                error="Surely pilot's name is longer than 3 characters?"
            ),
            Regexp(
                '^[a-zA-Z\-]+$', 
                error="Please enter pilot's full name, and be sure to "
                'only use capital letters, numbers, or dashes'
                )
            )
        )
    email = fields.String(required=True, validate=Email(
        error='Oops, try again! Your email seems wrong'
        )
    )
    password = fields.String(required=True, validate=Length(
        min=6,
        error="Let's use more than six characters for your password"
        )
    )
    status = fields.String(required=True, validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = (
            'id', 
            'arn', 
            'name', 
            'email', 
            'password',
            'status', 
            'is_admin'
            )

pilot_schema = PilotSchema()
pilots_schema = PilotSchema(many=True, exclude=['password'])


