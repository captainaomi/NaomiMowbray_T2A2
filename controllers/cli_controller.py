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
            name='Jack Sparrow',
            email='jack@captain.com',
            password=bcrypt.generate_password_hash('123abc').decode('utf-8'),
            status='inactive'
        )
    ]
    db.session.add_all(pilots)

    aircraft = [
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
    db.session.add_all(aircraft)

    flights = [
        Flight(
        pilot=pilots[2],
        aircraft=aircraft[1],
        date=date(2023, 7, 15),
        route='Moreton Island Scenic',
        landings=1,
        flight_time=1.40,
        ),
        Flight(
        pilot=pilots[2],
        aircraft=aircraft[1],
        date=date(2023, 7, 14),
        route='Brisbane Sunset Spectacular',
        landings=1,
        flight_time=0.33,
        ),
        Flight(
        pilot=pilots[1],
        aircraft=aircraft[3],
        date=date(2023, 7, 14),
        route='Western Bris Pub Crawl',
        landings=6,
        flight_time=2.31
        ),
    ]
    db.session.add_all(flights)

    expirations = [
        Expirations(
        pilot=pilots[2],
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