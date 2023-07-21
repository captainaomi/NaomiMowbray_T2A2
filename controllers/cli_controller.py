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
            arn=12345,
            name='Chief Pilot',
            email='admin@captain.com',
            password=bcrypt.generate_password_hash('123abc').decode('utf-8'),
            is_admin=True
        ),
        Pilot(
            arn='1079046',
            name='Captain Naomi',
            email='naomi@captain.com',
            password=bcrypt.generate_password_hash('123abc').decode('utf-8'),
        )
    ]
    db.session.add_all(pilots)

    aircraftz = [
        Aircraft(
            callsign='VH-CAX'
        ),
        Aircraft(
            callsign='VH-DEV'

        ),
        Aircraft(
            callsign='VH-WEB'
        ),
        Aircraft(
            callsign='VH-API'
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