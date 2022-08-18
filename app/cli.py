import os
import shutil
import random
import string
import re

import click
from config import Config
from faker import Faker

import app
from app import db
from app.models import Therapist, Client

def sanitize_string(userinput):
    clean =  re.sub('[^a-zA-Z0-9\u0590-\u05fe \-]+', '', userinput)
    # print(f"{userinput}  {clean}")
    return clean

faker = Faker('he_IL')

basedir = os.path.abspath(os.path.dirname(__file__))
migrations_dir = os.path.join(basedir, '../migrations')
db_path = app.Config.SQLALCHEMY_DATABASE_PATH
status = app.Config.LIVING_STATUS

def register(app):
    @app.cli.group()
    def fake():
        """Translation and localization commands."""
        pass
    @fake.command()
    def create_all():
        """Initialize a new DB."""
        if os.path.isdir(migrations_dir):
            shutil.rmtree(migrations_dir)

        if os.path.isfile(db_path):
            os.remove(db_path)

        if os.system('flask db init'):
            raise RuntimeError('flask db init command failed')

        if os.system('flask db migrate -m "Init tables"'):
            raise RuntimeError('flask db migrate -m "Init tables" command failed')

        if os.system('flask db upgrade'):
            raise RuntimeError('flask db upgrade command failed')

    @fake.command()
    def create_fake():
        """Initialize a fake DB."""

        if os.system('flask fake create-all'):
            raise RuntimeError('flask fake create-all command failed')

#         Create Therapists
        t = Therapist(
            username='ivanir',
            email='efi.ivanir@gmail.com',
            first_name='אפי',
            last_name='איוניר',
            tz_id='022397103',

            phone='0547884102',
            address_city='קרית טבעון',
            address_street='משה דיין',
            address_house_num='5/8',
        )
        t.set_password('123456')
        db.session.add(t)
        db.session.commit()

        t = Therapist(
            username='sungirl7',
            email='sungirl7@gmail.com',
            first_name='דנה',
            last_name='איוניר קליצקי',
            tz_id='333750875',

            phone='0547884102',
            address_city='קרית טבעון',
            address_street='משה דיין',
            address_house_num='5/8',
        )
        t.set_password('123456')
        db.session.add(t)
        db.session.commit()

        t = Therapist(
            username='pelegiv2',
            email='pelegiv2@gmail.com',
            first_name='פלג',
            last_name='איוניר',
            tz_id='333750877',

            phone='0547884122',
            address_city='קרית טבעון',
            address_street='משה דיין',
            address_house_num='5/8',
        )
        t.set_password('123456')
        db.session.add(t)
        db.session.commit()

        # Create clients db
        thera_id = []
        thera = Therapist.query.all()
        for t in thera:
            thera_id.append(t.id)

        for i in range(0,100):
            main_first_name = sanitize_string(faker.first_name_male())
            main_last_name = sanitize_string(faker.last_name())

            address_city = sanitize_string(faker.city_name())
            address_street = sanitize_string(faker.street_name())

            second_first_name = sanitize_string(faker.first_name_female())
            second_last_name = sanitize_string(faker.last_name())

            t = Client(
                main_first_name=main_first_name,
                main_last_name=main_last_name,

                address_city=address_city,
                address_street=address_street,
                address_house_num=faker.building_number(),

                therapist_id=random.choice(thera_id),

                second_first_name=second_first_name if i % 6 == 0 else '',
                second_last_name=second_last_name if i % 6 == 0 else '',

                main_birth_year=random.choice(range(1920,1950)),
                main_phone = faker.phone_number(),
                main_id = faker.ssn(),
                main_is_dutch = random.choice(('כן','לא')),
                main_is_davids = random.choice(('כן','לא')),
                main_status = random.choice(status),

                description = faker.text(max_nb_chars=200),

            )
            if i % 10 == 0:
                print(f"Complete {i} items")
            db.session.add(t)
            db.session.commit()


