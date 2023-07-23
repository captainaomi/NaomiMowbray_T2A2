from flask import Blueprint
from init import db, bcrypt
from models.pilot import Pilot
from models.flight import Flight
from models.aircraft import Aircraft
# from models.expirations import Expirations
from datetime import datetime, date


db_commands = Blueprint('db', __name__)


@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Your tables have been created')

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Your tables have been dropped')

@db_commands.cli.command('seed')
def seed_db():
    pilots = [
        Pilot(
            arn=100,
            name='Chief Pilot',
            email='chief@captain.com',
            password=bcrypt.generate_password_hash('123abc').decode('utf-8'),
            status='active',
            is_admin=True
        ),
        Pilot(
            arn='101',
            name='Captain Naomi',
            email='naomi@captain.com',
            password=bcrypt.generate_password_hash('123abc').decode('utf-8'),
            status='active'
        ),
        Pilot(
            arn='102',
            name='Captain Hook',
            email='hook@captain.com',
            password=bcrypt.generate_password_hash('123abc').decode('utf-8'),
            status='inactive'
        )
    ]
    db.session.add_all(pilots)

    aircraftz = [
        Aircraft(
            callsign='VH-CAX',
            status='active'
        ),
        Aircraft(
            callsign='VH-DEV',
            status='active'
        ),
        Aircraft(
            callsign='VH-WEB',
            status='active'
        ),
        Aircraft(
            callsign='VH-API',
            status='inactive'
        )
    ]
    db.session.add_all(aircraftz)

    flights = [
        Flight(
        pilot=pilots[1],
        aircraft=aircraftz[1],
        date=datetime(2023, 7, 15, 13, 0, 0),
        route='Moreton Island Scenic',
        landings=1,
        flight_time=1.40,
        ),

        Flight(
        pilot=pilots[1],
        aircraft=aircraftz[3],
        date=datetime(2023, 7, 14, 9, 3, 0),
        route='Western Bris Pub Crawl',
        landings=6,
        flight_time=2.31
        ),
    ]
    db.session.add_all(flights)

    db.session.commit()
    
    print('Your tables have been seeded')