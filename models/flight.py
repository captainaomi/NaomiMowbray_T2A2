from init import db, ma


class Flight(db.Model):
    __tablename__ = "flights"

    pilot_id = db.Column(
        db.Integer, db.ForeignKey('pilots.id'), nullable=False
        )
    aircraft_id = db.Column(
        db.Integer, db.ForeignKey('aircraftz.id'), nullable=False
        )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    route = db.Column(db.String(100), nullable=False)
    landings = db.Column(db.Integer, nullable=False)
    flight_time = db.Column(db.DECIMAL(5,2), nullable=False)

    pilot = db.relationship('Pilot', back_populates='flights')
    aircraft = db.relationship('Aircraft', back_populates='flights')
