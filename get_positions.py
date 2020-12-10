from app import db, headers
from models import Position
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)


# Position.__table__.drop(db.get_engine())
# Position.__table__.create(db.get_engine())

senator = Position(code='Sen.', name='Senator')
representative = Position(code='Rep.', name='Representative')



db.session.add_all([senator,representative])
db.session.commit()