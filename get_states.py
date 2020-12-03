from app import db, headers
from models import State
from fileread import FileRead
from utility import parse_state_data, get_members_json


State.__table__.drop(db.get_engine())
State.__table__.create(db.get_engine())

states = FileRead("states.txt")

for state in states.items:

    state_data = parse_state_data(state)

    new_state = State(acronym = state_data["acronym"], name=state_data["name"])
    db.session.add(new_state)

db.session.commit()




