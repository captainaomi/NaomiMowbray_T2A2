from init import ma

class PilotSchema(ma.Schema):    
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