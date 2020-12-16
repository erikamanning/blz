from app import db
from models import User
import pprint
pp = pprint.PrettyPrinter(indent=4)


# User.__table__.drop(db.get_engine())
User.__table__.create(db.get_engine())


