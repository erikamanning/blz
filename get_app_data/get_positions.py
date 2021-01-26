from app import db, headers
from models import Position
import requests

senator = Position(code='Sen.', name='Senator')
representative = Position(code='Rep.', name='Representative')
resident_commissioner = Position(code='R.C.', name='Resident Commissioner')
delegate = Position(code='Del.', name='Delegate')

db.session.add_all([senator,representative, resident_commissioner, delegate])
db.session.commit()