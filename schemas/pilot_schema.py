from init import ma
from marshmallow import fields
from marshmallow.validate import Email, OneOf


VALID_STATUSES = ('active', 'inactive')


class PilotSchema(ma.Schema):
    email = fields.String(validate=Email(
        error='Oops, try again! Your email seems wrong'
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