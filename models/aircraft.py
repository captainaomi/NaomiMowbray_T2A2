from init import db, ma
from marshmallow import fields
from marshmallow.validate import And, Length, Regexp

class Aircraft(db.Model):
    __tablename__ = 'aircraftz'

    id = db.Column(db.Integer, primary_key=True)
    callsign = db.Column(db.String(10), nullable=False)

    flights = db.relationship('Flight', back_populates='aircraft')

class AircraftSchema(ma.Schema):
    callsign = fields.String(required=True, validate=And(
        Length(max=10, error='Callsigns are not that long! Please use max. 10 characters'),    
        Regexp('^[a-zA-Z0-9.\-_]+$', error='Please only use letters, numbers, or dashes')
    ))

    class Meta:
        fields = ('id',)
        ordered = True

aircraft_schema = AircraftSchema()
aircraftz_schema = AircraftSchema(many=True)