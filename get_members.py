from app import db, headers, CURRENT_SESSION
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

# def extract_members(members_json, member_status):

#     members = []

#     for member in members_json:

#         if member_status:

#             members.append(member)

#     return members


# fix: Doesn't account for members who have changed their party- i.e. Justin Amash who would show as a duplicate
def save_members(members):

    # to commit all at once
    saved_members = []

    for member in members:

        mem_id = member['id']

        if not Member.query.filter(Member.id==mem_id).one_or_none():
            new_member = Member(id=mem_id,first_name=member['first_name'], last_name=member['last_name'], image= f'https://theunitedstates.io/images/congress/original/{mem_id}.jpg', state_id=member['state'], party_id=member['party'], position_code=member['short_title'], in_office=member['in_office'])

            print('****************************')
            print('Member In Office: ', member['in_office'])
            print('****************************')
            db.session.add(new_member)
            db.session.commit()

        else:

            # doesn't account for if state is changed
            existing_member = Member.query.filter(Member.id==mem_id).one_or_none()
            req = requests.get(member['api_uri'],headers=headers)
            json = req.json()
            entry = json['results'][0]
            existing_member_id = existing_member.id
            existing_member.first_name=entry['first_name'] 
            existing_member.last_name=entry['last_name'] 
            existing_member.party_id=entry['current_party'] 


            db.session.add(existing_member)
            db.session.commit()

def get_all_members(congress,chamber, member_status):

    members_json = get_members_json(congress,chamber)
    members = extract_members(members_json, member_status)
    save_members(members)


# get senate members
senate_members_json = get_members_json(CURRENT_SESSION,'senate')
# senate_members = extract_members(senate_members_json,True)
save_members(senate_members_json)


# get house members
house_members_json = get_members_json(CURRENT_SESSION,'house')
# house_members = extract_members(house_members_json,True)
save_members(house_members_json)


# seed command 
# python3 seed.py; python3 get_states.py; python3 get_positions.py; python3 get_parties.py; python3 get_members.py