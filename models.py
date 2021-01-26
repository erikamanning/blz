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
    bill_id = db.Column(db.String, db.ForeignKey('bills.id', ondelete="CASCADE"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)

    def __repr__(self):

        return f'BillFollow: username: {self.username}, bill_id: {self.bill_id}'

class SponsoredBill(db.Model):

    __tablename__ = 'sponsored_bills'

    bill_id = db.Column(db.String, db.ForeignKey('bills.id', ondelete="CASCADE"), primary_key=True)
    sponsor_id = db.Column(db.String, db.ForeignKey('legislators.id', ondelete="CASCADE"), primary_key=True)

    def __repr__(self):

        return f'Sponsored Bill: sponsor_id: {self.sponsor_id}, bill_id: {self.bill_id}'

class Bill(db.Model):

    __tablename__ = "bills"

    id = db.Column(db.String, primary_key=True, nullable = False, unique=True)
    bill_slug = db.Column(db.String, nullable = False)
    congress = db.Column(db.Integer, nullable = False)
    title = db.Column(db.String, nullable = False)
    short_title = db.Column(db.String, nullable = True)
    sponsor_id = db.Column(db.String, db.ForeignKey('legislators.id', ondelete="CASCADE"), nullable = False)
    congressdotgov_url = db.Column(db.String, nullable = False)
    introduced_date = db.Column(db.String, nullable = False)
    primary_subject = db.Column(db.String, nullable = False)
    latest_major_action_date = db.Column(db.String, nullable = True)
    latest_major_action = db.Column(db.String, nullable = True)
    summary = db.Column(db.String, nullable = True)
    summary_short = db.Column(db.String, nullable = True)

    sponsor = db.relationship('SponsoredBill', backref="bills", cascade="all, delete")

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

class Legislator(db.Model):

    __tablename__ = "legislators"

    id = db.Column(db.String, primary_key=True, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image = db.Column(db.String,nullable=True)
    state_id = db.Column(db.String, db.ForeignKey('states.acronym'), nullable=False)
    party_id = db.Column(db.String,db.ForeignKey('parties.code'),nullable=False)
    position_code = db.Column(db.String, db.ForeignKey('positions.code'), nullable=False)

    website = db.Column(db.String,nullable=False)
    in_office = db.Column(db.Boolean, primary_key= True, nullable=False)
    twitter_account = db.Column(db.String, default='Not Listed',nullable=True)
    facebook_account = db.Column(db.String, default='Not Listed',nullable=True)
    youtube_account = db.Column(db.String, default='Not Listed',nullable=True)
    office_address = db.Column(db.String, default='Not Listed',nullable=False)
    phone = db.Column(db.String,default='Not Listed',nullable=False)

    state = db.relationship('State', backref='legislators')
    party = db.relationship('Party', backref='legislators')
    position = db.relationship('Position', backref='legislators')

    sponsored_bills = db.relationship('SponsoredBill', backref='legislators', cascade="all, delete")

class State(db.Model):

    __tablename__ = "states"

    acronym = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):

        return f'State: {self.name}, {self.acronym}'

class Position(db.Model):

    __tablename__ = "positions"

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Party(db.Model):

    __tablename__ = "parties"

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

class User(db.Model):

    __tablename__ = "users"

    @classmethod
    def register(cls, username, password, email, state_id=''):
        """ Register user w/hashed password & return user. """

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, state_id=state_id)
        
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
    
    @classmethod
    def check_for_duplicate_username(cls, new_username):

        """ 
            Checks if username is not already in system. Returns True if not,
            False if the username already exists.

        """
        if User.query.filter(User.username == new_username).one_or_none():

            return False
        
        else:

            return True

    @classmethod
    def check_for_duplicate_email(cls, new_email):

        """ 
            Checks if email is not already in system. Returns True if not,
            False if the email already exists.

        """
        if User.query.filter(User.email == new_email).one_or_none():

            return False
        
        else:

            return True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False,unique=True)
    state_id = db.Column(db.String, db.ForeignKey('states.acronym'), nullable=True)

    state = db.relationship('State', backref='users')

    followed_bills=db.relationship(
        'Bill', 
        secondary='bill_follows',
        primaryjoin=(BillFollows.user_id == id),
        cascade="all, delete"
    )

    def edit_profile_check(self, username, email):
        
        data_check = {

            'username_check': True,
            'email_check'   : True
        }

        if username != self.username:

            new_username_check = User.check_for_duplicate_username(username)
            data_check['username_check'] = new_username_check

        if email != self.email:

            new_email_check = User.check_for_duplicate_email(email) 
            data_check['email_check'] = new_email_check

        return data_check

    def edit_profile(self,username,email,state_id):

        changes_made = False

        if self.username!=username:

            self.username=username
            changes_made = True

        if self.email!=email:

            self.email=email
            changes_made = True

        if self.state_id!=state_id:

            self.state_id=state_id
            changes_made = True

        db.session.add(self)
        db.session.commit()

        return changes_made

    def change_password(self, new_password):

        hashed = bcrypt.generate_password_hash(new_password)

        hashed_utf8 = hashed.decode("utf8")

        self.password = hashed_utf8

    def __repr__(self):

        return f'User: {self.username}'
