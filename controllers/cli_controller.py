from flask import Blueprint
from init import db, bcrypt
from models.pilot import Pilot
from models.flight import Flight
from models.aircraft import Aircraft
from models.expirations import Expirations
from datetime import date


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
            arn=10,
            name='Doctor Who',
            email='doctorwho@captain.com',
            password=bcrypt.generate_password_hash('123abc').decode('utf-8'),
            status='active',
            is_admin=True
        ),
        Pilot(
            arn='11',
            name='Rose Tyler',
            email='rose@captain.com',
            password=bcrypt.generate_password_hash('123abc').decode('utf-8'),
            status='active'
        ),
        Pilot(
            arn='12',
            name='Amy Pond',
            email='amy@captain.com',
            password=bcrypt.generate_password_hash('123abc').decode('utf-8'),
            status='active'
        ),
        Pilot(
            arn='13',
            name='Sarah Jane',
            email='sarah@captain.com',
            password=bcrypt.generate_password_hash('123abc').decode('utf-8'),
            status='inactive'
        ),
    ]
    db.session.add_all(pilots)

    aircraft = [
        Aircraft(
            callsign='VH-TARDIS',
            status='active'
        ),
        Aircraft(
            callsign='VH-BIGBEN',
            status='inactive'
        ),
        Aircraft(
            callsign='VH-TIMEY',
            status='active'
        ),
        Aircraft(
            callsign='VH-K-9',
            status='active'
        )
    ]
    db.session.add_all(aircraft)

    flights = [
        Flight(
        pilot=pilots[0],
        aircraft=aircraft[0],
        date=date(1998, 7, 15),
        route='Gallifrey Recon',
        landings=1,
        flight_time=1.40,
        ),
        Flight(
        pilot=pilots[1],
        aircraft=aircraft[0],
        date=date(2015, 6, 11),
        route='Bad Wolf Bay Drop Off',
        landings=2,
        flight_time=0.33,
        ),
        Flight(
        pilot=pilots[3],
        aircraft=aircraft[3],
        date=date(2011, 10, 11),
        route='London Pub Crawl',
        landings=6,
        flight_time=2.31
        ),
    ]
    db.session.add_all(flights)

    expirations = [
        Expirations(
        pilot=pilots[0],
        medical=date(2023, 12, 31),
        biannual_review=date(2024, 3, 15),
        company_review=date(2000, 7, 1),
        dangerous_goods=date(2023, 5, 26),
        asic=date(2023, 10, 9),
        ),
        Expirations(
        pilot=pilots[1],
        medical=date(1999, 9, 9),
        biannual_review=date(2030, 2, 22),
        company_review=date(1998, 3, 3),
        dangerous_goods=date(2012, 4, 4),
        ),
    ]
    db.session.add_all(expirations)
    db.session.commit()
    
    print('Your tables have been seeded')