from app import db
from models import BillFollows
import pprint
pp = pprint.PrettyPrinter(indent=4)


BillFollows.__table__.drop(db.get_engine())
BillFollows.__table__.create(db.get_engine())


