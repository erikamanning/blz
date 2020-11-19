from app import db, headers
from models import Subject, PolicyArea, State, Chamber, Position
from fileread import FileRead
from utility import parse_state_data, get_members_json

db.drop_all()
db.create_all()

subjects = FileRead("subjects.txt")
policy_areas = FileRead("policy_areas.txt")
states = FileRead("states.txt")



for sub in subjects.items:

    newSubject = Subject(name=sub)
    db.session.add(newSubject)


for pa in policy_areas.items:

    new_pa = PolicyArea(name=pa)
    db.session.add(new_pa)

for state in states.items:

    state_data = parse_state_data(state)

    new_state = State(acronym = state_data["acronym"], name=state_data["name"])
    db.session.add(new_state)

# chambers
senate = Chamber(chamber_code="SEN",name="Senate")
house = Chamber(chamber_code="HSE",name="House of Representatives")
db.session.add_all([senate,house])


# positions
senator = Position(position_code="sen",name="Senator")
representative = Position(position_code="rep",name="Representative")
db.session.add_all([senator,representative])

# members
senators = get_members_json("senate")
representatives = get_members_json("house")

db.session.add_all(senators)
db.session.add_all(representatives)

db.session.commit()




