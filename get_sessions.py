from app import db, headers, CURRENT_SESSION
from models import Session
import requests

sessions = []

for x in range(116,int(CURRENT_SESSION)+1):

    new_session = Session(id=x)
    sessions.append(new_session)


db.session.add_all(sessions)
db.session.commit()