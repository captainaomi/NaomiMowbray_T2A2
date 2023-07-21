from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf

class Flight(db.Model):
    __tablename__ = "flights"

    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraftz.id'), nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    route = db.Column(db.String(100), nullable=False)
    landings = db.Column(db.Integer, nullable=False)
    flight_time = db.Column(db.DECIMAL(5,2), nullable=False)

    pilot = db.relationship('Pilot', back_populates='flights')
    aircraft = db.relationship('Aircraft', back_populates='flights')

class FlightSchema(ma.Schema):
    pilot = fields.Nested('PilotSchema', only=['id', 'arn', 'name'])
    aircraft = ('AircraftSchema',)

    route = fields.String(required=True, validate=And(
        Length(min=10, error='Route must be at least ten characters long'),
        Regexp('^[a-zA-Z0-9.\-_. ]+$', error='Please only use letters, numbers, dashes or spaces')
    ))

    class Meta:
        fields = ('pilot_id', 'aircraft_id', 'id', 'date', 'route', 'landings', 'flight_time')
        ordered = True

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)
