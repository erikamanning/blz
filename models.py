from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


db = SQLAlchemy()

def connect_db(app):
    """ Connect to database."""

    db.app = app
    db.init_app(app)

class BillFollows(db.Model):

    __tablename__ = 'bill_follows'

    # may want to change username to user id to save processing time later
    bill_id = db.Column(db.String, db.ForeignKey('bills.id'), primary_key=True)
    username = db.Column(db.String, db.ForeignKey('users.username'), primary_key=True)

    def __repr__(self):

        return f'BillFollow: username: {self.username}, bill_id: {self.bill_id}'


class Bill(db.Model):

    __tablename__ = "bills"

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

    # sponsor = db.relationship('Member', backref="members")

    def __repr__(self):

        return 'Bill: {self.title}'


class Subject(db.Model):

    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

class PolicyArea(db.Model):

    __tablename__ = "policy_areas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

class Member(db.Model):

    __tablename__ = "members"

    id = db.Column(db.String, primary_key=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    state_id = db.Column(db.String(2), db.ForeignKey('states.acronym'), nullable=False)
    party_id = db.Column(db.String,db.ForeignKey('parties.code'),nullable=False)
    position_code = db.Column(db.String, db.ForeignKey('positions.code'), nullable=False)
    in_office = db.Column(db.Boolean, nullable=False)

    state = db.relationship('State', backref='members')
    party = db.relationship('Party', backref='members')
    position = db.relationship('Position', backref='members')

class State(db.Model):

    __tablename__ = "states"

    acronym = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):

        return f'State: {self.name}, {self.acronym}'

class User(db.Model):

    __tablename__ = "users"

    @classmethod
    def register(cls, username, password, email):
        """ Register user w/hashed password & return user. """

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email)
        
    @classmethod
    def authenticate(cls, username, password):

        """ 
            Validate that user exists & password is correct. 
        
            Return the user if valid; else return False

        """
        u = User.query.filter_by(username=username).first()

        # check if user exists and if password is the correct password
        if u and bcrypt.check_password_hash(u.password,password):
            #return user instance
            return u
        
        else:
            return False


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False,unique=True)
    state_id = db.Column(db.String(2), nullable=True)

    followed_bills=db.relationship(
        'Bill', 
        secondary='bill_follows',
        primaryjoin=(BillFollows.username == username)
    )

    def __repr__(self):

        return f'User: {self.username}'


class Position(db.Model):

    __tablename__ = "positions"

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Party(db.Model):

    __tablename__ = "parties"

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

# classes to add later

# class Chamber(db.Model):

#     __tablename__ = "chambers"

#     chamber_code = db.Column(db.String(3), primary_key=True)
#     name = db.Column(db.String, nullable=False)

# class Vote(db.Model):
#     __tablename__ = "votes"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     member_id = db.Column(db.String, db.ForeignKey('members.id'), nullable=False)
#     bill_id = db.Column(db.String, db.ForeignKey('bills.id'), nullable=False)
#     vote_position = db.Column(db.String, nullable=False)