from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


db = SQLAlchemy()

def connect_db(app):
    """ Connect to database."""

    db.app = app
    db.init_app(app)


class Bill(db.Model):

    __tablename__ = "bills"

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    sponsor_id = db.Column(db.String, db.ForeignKey('members.id'),
        nullable=False)

class Subject(db.Model):

    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

class PolicyArea(db.Model):

    __tablename__ = "policy_areas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

class State(db.Model):

    __tablename__ = "states"

    acronym = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String, nullable=False)


class Member(db.Model):

    __tablename__ = "members"

    id = db.Column(db.String, primary_key=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    state_id = db.Column(db.String, nullable=False)
    party_id = db.Column(db.String(2), nullable=False)
    position_code = db.Column(db.String(3), nullable=False)

class Chamber(db.Model):

    __tablename__ = "chambers"

    chamber_code = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String, nullable=False)

class Position(db.Model):

    __tablename__ = "positions"

    position_code = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String, nullable=False)

class Vote(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.String, db.ForeignKey('members.id'), nullable=False)
    bill_id = db.Column(db.String, db.ForeignKey('bills.id'), nullable=False)
    response = db.Column(db.String, nullable=False)