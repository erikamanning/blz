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

    # id = db.Column(db.String, primary_key=True)
    # title = db.Column(db.String, nullable=False)
    # sponsor_id = db.Column(db.String, db.ForeignKey('members.id'),
    #     nullable=False)

    id = db.Column(db.String, primary_key=True, nullable = False)
    bill_slug = db.Column(db.String, nullable = False)
    congress = db.Column(db.String, nullable = False)
    bill = db.Column(db.String, nullable = False)
    bill_type = db.Column(db.String, nullable = False)
    number = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    short_title = db.Column(db.String, nullable = True)
    sponsor_id = db.Column(db.String, nullable = False)
    congressdotgov_url = db.Column(db.String, nullable = False)
    introduced_date = db.Column(db.String, nullable = False)
    active = db.Column(db.Boolean, nullable = False)
    last_vote = db.Column(db.String, nullable = True)
    house_passage = db.Column(db.String, nullable = True)
    senate_passage = db.Column(db.String, nullable = True)
    enacted = db.Column(db.String, nullable = True)
    vetoed = db.Column(db.String, nullable = True)
    primary_subject = db.Column(db.String, nullable = True)
    committees = db.Column(db.String, nullable = True)
    committee_codes = db.Column(db.String, nullable = True)
    latest_major_action_date = db.Column(db.String, nullable = True)
    latest_major_action = db.Column(db.String, nullable = True)
    house_passage_vote = db.Column(db.String, nullable = True)
    senate_passage_vote = db.Column(db.String, nullable = True)
    summary = db.Column(db.String, nullable = True)
    summary_short = db.Column(db.String, nullable = True)


    def __repr__(self):

        return 'Bill: {self.title}'

# class Vote(db.Model):

#     __tablename__ = "votes"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     member_id = db.Column(db.String, db.ForeignKey('members.id'), nullable=False)
#     bill_id = db.Column(db.String, db.ForeignKey('bills.id'), nullable=False)
#     vote_position = db.Column(db.String, nullable=False)


class Subject(db.Model):

    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

class PolicyArea(db.Model):

    __tablename__ = "policy_areas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

# class State(db.Model):

#     __tablename__ = "states"

#     acronym = db.Column(db.String(2), primary_key=True)
#     name = db.Column(db.String, nullable=False)


# class Member(db.Model):

#     __tablename__ = "members"

#     id = db.Column(db.String, primary_key=True, nullable=False)
#     first_name = db.Column(db.String, nullable=False)
#     last_name = db.Column(db.String, nullable=False)
#     state_id = db.Column(db.String, nullable=False)
#     party_id = db.Column(db.String(2), nullable=False)
#     position_code = db.Column(db.String(3), nullable=False)

# class Chamber(db.Model):

#     __tablename__ = "chambers"

#     chamber_code = db.Column(db.String(3), primary_key=True)
#     name = db.Column(db.String, nullable=False)

# class Position(db.Model):

#     __tablename__ = "positions"

#     position_code = db.Column(db.String(5), primary_key=True)
#     name = db.Column(db.String, nullable=False)
