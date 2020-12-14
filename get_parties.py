from app import db, headers
from models import Party
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)


# Party.__table__.drop(db.get_engine())
# Party.__table__.create(db.get_engine())

republican = Party(code='R', name='Republican')
democrat = Party(code='D', name='Democrat')
independent_democrat = Party(code='ID', name='Independent Democrat')
independent = Party(code='I', name='Independent')
libertarian = Party(code='LP', name='Libertarian')
green_party = Party(code='GP', name="Green Party")


db.session.add_all([republican,democrat,independent, independent_democrat,libertarian,green_party])
db.session.commit()