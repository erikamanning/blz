from app import db, headers
from models import Session
import requests

Session.__table__.drop(db.get_engine())
Session.__table__.create(db.get_engine())

CURRENT_SESSION = 116

sessions = []

for x in range(103,CURRENT_SESSION+1):

    new_session = Session(id=x)
    sessions.append(new_session)


db.session.add_all(sessions)
db.session.commit()