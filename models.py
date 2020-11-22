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

# class Vote(db.Model):

#     __tablename__ = "votes"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     member_id = db.Column(db.String, db.ForeignKey('members.id'), nullable=False)
#     bill_id = db.Column(db.String, db.ForeignKey('bills.id'), nullable=False)
#     vote_position = db.Column(db.String, nullable=False)


    

    # chamber": "House",
    # date": "2017-09-05",
    # time": "19:07:00",
    # roll_call": "440",
    # question": "On Motion to Suspend the Rules and Pass, as Amended",
    # result": "Passed",
    # total_yes": 403,
    # total_no": 3,
    # total_not_voting": 28,
    # api_url": "https://api.propublica.org/congress/v1/115/house/sessions/1/votes/440.json"


#       "bill_id": "hr2864-115",
#       "bill_slug": "hr2864",
#       "congress": "115",
#       "bill": "H.R.2864",
#       "bill_type": "hr",
#       "number": "H.R.2864",
#       "bill_uri": "https://api.propublica.org/congress/v1/115/bills/hr2864.json",
#       "title": "To direct the Securities and Exchange Commission to allow certain issuers to be exempt from registration requirements, and for other purposes.",
#       "short_title": "Improving Access to Capital Act",
#       "sponsor_title": "Rep.",
#       "sponsor": "Kyrsten Sinema",
#       "sponsor_id": "S001191",
#       "sponsor_uri": "https://api.propublica.org/congress/v1/members/S001191.json",
#       "sponsor_party": "D",
#       "sponsor_state": "AZ",
#       "gpo_pdf_uri": null,
#       "congressdotgov_url": "https://www.congress.gov/bill/115th-congress/house-bill/2864",
#       "govtrack_url": "https://www.govtrack.us/congress/bills/115/hr2864",
#       "introduced_date": "2017-06-08",
#       "active": true,
#       "last_vote": "2017-09-05",
#       "house_passage": "2017-09-05",
#       "senate_passage": null,
#       "enacted": null,
#       "vetoed": null,
#       "cosponsors": 5,
#       "withdrawn_cosponsors": 0,
#       "primary_subject": "Finance and Financial Sector",
#       "committees": "Senate Banking, Housing, and Urban Affairs Committee",
#       "committee_codes": [
#         "SSBK",
#         "HSBA"
#       ],
#       "latest_major_action_date": "2017-09-06",
#       "latest_major_action": "Received in the Senate and Read twice and referred to the Committee on Banking, Housing, and Urban Affairs.",
#       "house_passage_vote": "2017-09-05",
#       "senate_passage_vote": null,
#       "summary": "(Sec. 1) This bill exempts, under Regulation A+, certain fully reporting issuers of securities from specified disclosure requirements. Under current law, Regulation A+ exempts certain smaller offerings from securities registration requirements but applies only to non-reporting issuers. ",
#       "summary_short": "(Sec. 1) This bill exempts, under Regulation A+, certain fully reporting issuers of securities from specified disclosure requirements. Under current law, Regulation A+ exempts certain smaller offerings from securities registration requirements but applies only to non-reporting issuers. ",
#       "cbo_estimate_url": "https://www.cbo.gov/publication/53069",

#       "votes": [
#         {
#           "chamber": "House",
#           "date": "2017-09-05",
#           "time": "19:07:00",
#           "roll_call": "440",
#           "question": "On Motion to Suspend the Rules and Pass, as Amended",
#           "result": "Passed",
#           "total_yes": 403,
#           "total_no": 3,
#           "total_not_voting": 28,
#           "api_url": "https://api.propublica.org/congress/v1/115/house/sessions/1/votes/440.json"
#         }
#       ]



# class Subject(db.Model):

#     __tablename__ = "subjects"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String, nullable=False)

# class PolicyArea(db.Model):

#     __tablename__ = "policy_areas"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String, nullable=False)

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
