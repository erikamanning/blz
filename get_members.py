from app import db, headers
from models import Member
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)


# add cascade

# Member.__table__.drop(db.get_engine())
# Member.__table__.create(db.get_engine())

def get_members_json(congress, chamber):

    req = requests.get(f'https://api.propublica.org/congress/v1/{congress}/{chamber}/members.json', headers=headers)

    json = req.json()

    members_json = json['results'][0]['members']

    return members_json

def extract_members(members_json, member_status):

    members = []

    for member in members_json:

        if member_status:

            members.append(member)


    return members

def save_members(members):

    saved_members = []

    for member in members:

        new_member = Member(congress_id=member['id'],first_name=member['first_name'], last_name=member['last_name'], state_id=member['state'], party_id=member['party'], position_code=member['short_title'], in_office=member['in_office'])

        saved_members.append(new_member)


    db.session.add_all(saved_members)
    db.session.commit()

def get_all_members(congress,chamber, member_status):

    members_json = get_members_json(congress,chamber)
    members = extract_members(members_json, member_status)
    save_members(members)


# get senate members
senate_members_json = get_members_json(116,'senate')
senate_members = extract_members(senate_members_json,True)
save_members(senate_members)


# get house members
house_members_json = get_members_json(116,'house')
house_members = extract_members(house_members_json,True)
save_members(house_members)


# seed command python3 seed.py; python3 get_states.py; python3 get_positions.py; python3 get_parties.py; python3 get_members.py