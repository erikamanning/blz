from app import db, headers
from models import Party
import requests

republican = Party(code='R', name='Republican')
democrat = Party(code='D', name='Democrat')
independent_democrat = Party(code='ID', name='Independent Democrat')
independent = Party(code='I', name='Independent')
libertarian = Party(code='LP', name='Libertarian')
green_party = Party(code='GP', name="Green Party")

db.session.add_all([republican,democrat,independent, independent_democrat,libertarian,green_party])
db.session.commit()