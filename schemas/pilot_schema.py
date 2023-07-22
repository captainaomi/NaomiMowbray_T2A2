from init import ma
from marshmallow import fields
from marshmallow.validate import Email, Length


class PilotSchema(ma.Schema):    
    email = fields.String(validate=Email)
    password = fields.String(validate=Length(min=6))

    class Meta:
        fields = (
            'id', 
            'arn', 
            'name', 
            'email', 
            'password', 
            'is_admin'
            )


pilot_schema = PilotSchema(exclude=['password'])
pilots_schema = PilotSchema(many=True, exclude=['password'])