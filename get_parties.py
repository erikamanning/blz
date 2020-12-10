from app import db, headers
from models import Party
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)


# Party.__table__.drop(db.get_engine())
# Party.__table__.create(db.get_engine())

republican = Party(code='R', name='Republican')
democrat = Party(code='D', name='Democrat')
independent = Party(code='ID', name='Independent')
libertarian = Party(code='LP', name='Libertarian')
green_party = Party(code='GP', name="Green Party")


db.session.add_all([republican,democrat,independent,libertarian,green_party])
db.session.commit()