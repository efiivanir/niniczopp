from hashlib import md5

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user

from app import login


@login.user_loader
def load_user(id):
    return Therapist.query.get(int(id))


class Therapist(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True,nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    tz_id = db.Column(db.String(9), index=True, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    phone = db.Column(db.String(15))
    address_city = db.Column(db.String(64))
    address_street = db.Column(db.String(64))
    address_house_num = db.Column(db.String(64))
    clients = db.relationship('Client', backref='therapist', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<Therapist {}>'.format(self.username)

    def user_clients(self):
        clients = Client.query.filter_by(therapist_id=self.id)
        return clients


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    main_first_name = db.Column(db.String(64), nullable=False)
    main_last_name = db.Column(db.String(64), nullable=False)
    main_id = db.Column(db.String(10))
    main_birth_year = db.Column(db.Integer)
    main_phone = db.Column(db.String(15))
    main_is_dutch = db.Column(db.String(2))
    main_is_davids = db.Column(db.String(2))
    main_status = db.Column(db.String(15))

    second_first_name = db.Column(db.String(64))
    second_last_name = db.Column(db.String(64))
    second_id = db.Column(db.String(10))
    second_birth_year = db.Column(db.Integer)
    second_phone = db.Column(db.String(15))
    second_is_dutch = db.Column(db.String(12))
    second_status = db.Column(db.String(15))

    address_city = db.Column(db.String(64), nullable=False)
    address_street = db.Column(db.String(64), nullable=False)

    address_house_num = db.Column(db.String(64), nullable=False)

    description = db.Column(db.String(200))

    therapist_id = db.Column(db.Integer,
                             db.ForeignKey('therapist.id'),
                             nullable=False)

    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint(main_first_name,
                                          main_last_name,
                                          address_city,
                                          address_street,
                                          address_house_num),)

    def __repr__(self):
        return '<Client {} {} >'.format(self.main_first_name, self.main_last_name)


