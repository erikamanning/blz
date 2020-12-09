from app import db, headers
from models import Member
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)


# Member.__table__.drop(db.get_engine())
Member.__table__.create(db.get_engine())

def get_members_json(congress, chamber):

    req = requests.get(f'https://api.propublica.org/congress/v1/{congress}/{chamber}/members.json', headers=headers)

    json = req.json()

    members_json = json['results'][0]['members']

    return members_json

def extract_members(members_json, member_status):

    members = []

    for member in members_json:

        if member['in_office'] == member_status:

            members.append(member)

            print('member: ', member)

    return members

def save_members(members):

    saved_members = []

    for member in members:

        new_member = Member(id=member['id'],first_name=member['first_name'], last_name=member['last_name'], state_id=member['state'], party_id=member['party'], position_code=member['short_title'], in_office=member['in_office'])

        saved_members.append(new_member)


    db.session.add_all(saved_members)
    db.session.commit()

def get_all_members(congress,chamber, member_status):

    members_json = get_members_json(congress,chamber,member_status)
    members = extract_members
    save_members(members)


members_json = get_members_json(116,'senate')
print("***********************************")
print("Members Json: ")
pp.pprint(members_json)
print("***********************************")

members = extract_members(members_json,True)
print("***********************************")
print("Members Json: ")
pp.pprint(members)
print("***********************************")


save_members(members)

# get_all_members(116,'senate', 'in_office')