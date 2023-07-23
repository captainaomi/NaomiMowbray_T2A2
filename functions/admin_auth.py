from init import db
from models.pilot import Pilot

from flask_jwt_extended import get_jwt_identity
import functools

def admin_authorisation(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        pilot_id = get_jwt_identity()
        stmt = db.select(Pilot).filter_by(id=pilot_id)
        pilot = db.session.scalar(stmt)
        if pilot.is_admin:
            return fn(*args, **kwargs)
        else:
            return {
                'Error': 'Nope, admins only for those shenanigans'
                }, 403
    return wrapper