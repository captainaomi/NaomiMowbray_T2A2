from init import db


class Pilot(db.Model):
    __tablename__ = 'pilot'

    id = db.Column(db.Integer, primary_key=True)
    arn = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    flight = db.relationship('Flight', back_populates='pilot')
    expirations = db.relationship('Expirations', back_populates='pilot')