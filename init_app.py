from app import db

db.drop_all()
db.create_all()

'''

    bash command:
    python3 get_states.py; python3 get_positions.py; python3 get_parties.py; python3 get_members.py ; python3 get_bills.py ; python3 get_policy_areas.py ; python3 get_sessions.py

'''
import init_app 
import get_states
import get_positions
import get_parties
import get_members
import get_bills
import get_policy_areas
import get_sessions
