from app import db, headers
from models import State, Position, Party, Member
from fileread import FileRead
from utility import parse_state_data, get_members_json

# this order works, explain why

Member.__table__.drop(db.get_engine())
State.__table__.drop(db.get_engine())
Position.__table__.drop(db.get_engine())
Party.__table__.drop(db.get_engine())


Party.__table__.create(db.get_engine())
Position.__table__.create(db.get_engine())
State.__table__.create(db.get_engine())
Member.__table__.create(db.get_engine())

