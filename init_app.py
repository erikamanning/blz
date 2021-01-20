from app import db

db.drop_all()
db.create_all()


import get_states
import get_positions
import get_parties
import get_legislators
import get_bills
import get_policy_areas
