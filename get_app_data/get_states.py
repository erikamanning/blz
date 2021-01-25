from app import db
from models import State
from get_app_data.fileread import FileRead

# separates state name string from acronym string and removes space from beginning of acronym string
def parse_state_data(state_str):

    split_data = state_str.split(",")

    state_data = {
        "name": split_data[0],
        "acronym":split_data[1].strip()
    }

    return state_data




# get state data
states = FileRead("get_app_data/states.txt")

for state in states.items:

    state_data = parse_state_data(state)

    new_state = State(acronym = state_data["acronym"], name=state_data["name"])
    db.session.add(new_state)

db.session.commit()