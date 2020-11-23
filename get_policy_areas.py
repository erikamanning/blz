from app import db, headers
from models import PolicyArea, Bill
import requests

PolicyArea.__table__.drop(db.get_engine())
PolicyArea.__table__.create(db.get_engine())


# must filter out empy subject fields from bill table
policy_areas = db.session.query(Bill.primary_subject.distinct()).filter(Bill.primary_subject != '').order_by(Bill.primary_subject.asc()).all()

def save_policy_areas(policy_areas):

    saved_policy_areas = []

    # convert from tuples
    for policy_area in policy_areas:

        new_policy_area = PolicyArea(name=policy_area[0])
        saved_policy_areas.append(new_policy_area)


    print(saved_policy_areas)
    db.session.add_all(saved_policy_areas)
    db.session.commit()


save_policy_areas(policy_areas)
