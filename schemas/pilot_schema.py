from init import ma
from marshmallow import fields
from marshmallow.validate import Email, Length


class PilotSchema(ma.Schema):    
    email = fields.String(validate=
        Email(error='Oops, try again! Your email seems wrong'))

    class Meta:
        fields = (
            'id', 
            'arn', 
            'name', 
            'email', 
            'password', 
            'is_admin'
            )

pilot_schema = PilotSchema()
pilots_schema = PilotSchema(many=True, exclude=['password'])