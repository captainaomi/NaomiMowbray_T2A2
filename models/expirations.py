from init import db


class Expirations(db.Model):
    __tablename__ = 'expirations'

    id = db.Column(db.Integer, primary_key=True)
    # Include pilot using foreign key
    pilot_id = db.Column(
        db.Integer, db.ForeignKey('pilot.id'), nullable=False, unique=True
        )
    medical = db.Column(db.Date, nullable=False)
    biannual_review = db.Column(db.Date, nullable=False)
    company_review = db.Column(db.Date, nullable=False)
    dangerous_goods = db.Column(db.Date, nullable=False)
    asic = db.Column(db.Date)

    pilot = db.relationship('Pilot', back_populates='expirations')