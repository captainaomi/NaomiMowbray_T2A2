from init import db, ma
from marshmallow import fields
from marshmallow.validate import And, Regexp

class Pilot(db.Model):
    __tablename__ = 'pilots'

    id = db.Column(db.Integer, primary_key=True)
    arn = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    flights = db.relationship('Flight', back_populates='pilot')

class PilotSchema(ma.Schema):
    # arn = fields.Integer(required=True, validate=
    #     Regexp('^[0-9]+$', error='Your ARN should be written with numbers only')
    # )
    
    class Meta:
        fields = ('id', 'arn', 'name', 'email', 'password', 'is_admin')

pilot_schema = PilotSchema(exclude=['password'])
pilots_schema = PilotSchema(many=True, exclude=['password'])