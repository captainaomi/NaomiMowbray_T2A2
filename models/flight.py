from init import db


class Flight(db.Model):
    __tablename__ = 'flight'

    # Include pilot and aircraft using their foreign keys
    pilot_id = db.Column(
        db.Integer, db.ForeignKey('pilot.id'), nullable=False
        )
    aircraft_id = db.Column(
        db.Integer, db.ForeignKey('aircraft.id'), nullable=False
        )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    route = db.Column(db.String(100), nullable=False)
    landings = db.Column(db.Integer, nullable=False)
    flight_time = db.Column(db.DECIMAL(4,2), nullable=False)


    pilot = db.relationship('Pilot', back_populates='flight')
    aircraft = db.relationship('Aircraft', back_populates='flight')
