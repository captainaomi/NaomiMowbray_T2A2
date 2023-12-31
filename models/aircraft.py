from init import db


class Aircraft(db.Model):
    __tablename__ = 'aircraft'

    id = db.Column(db.Integer, primary_key=True)
    callsign = db.Column(db.String(10), nullable=False, unique=True)
    status = db.Column(db.String, nullable=False)

    flight = db.relationship('Flight', back_populates='aircraft')