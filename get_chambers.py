from app import db, headers
from models import Chamber
import requests

# Chamber.__table__.drop(db.get_engine())
Chamber.__table__.create(db.get_engine())

senate=Chamber(code='sen', name='Senate')
house=Chamber(code='hse', name='House of Representatives')
both=Chamber(code='bth', name='Senate & House of Representatives')
