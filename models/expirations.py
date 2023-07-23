from init import db

class Expirations(db.Model):
    __tablename__ = "expirations"

    pilot_id = db.Column(
        db.Integer, db.ForeignKey('pilots.id'), nullable=False
        )

    id = db.Column(db.Integer, primary_key=True)
    medical = db.Column(db.DATE, nullable=False)
    biannual_review = db.Column(db.DATE, nullable=False)
    company_review = db.Column(db.Date, nullable=False)
    dangerous_goods = db.Column(db.Date, nullable=False)
    asic = db.Column(db.Date)

    pilot = db.relationship('Pilot', back_populates='expirations')