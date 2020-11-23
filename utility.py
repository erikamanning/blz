import requests
from models import Member, Vote

from secrets import API_SECRET_KEY


headers = {'X-API-Key': API_SECRET_KEY}

# debug string
# print("***********************************")
# print("Subject name for query: ", subject_name)
# print("***********************************")


# separates state name string from acronym string and removes space from beginning of acronym string, 
# could also just delete space from local text file
def parse_state_data(state_str):

    split_data = state_str.split(",")

    state_data = {
        "name": split_data[0],
        "acronym":split_data[1].strip()
    }

    return state_data

def cure_query_str(query_str):
    query_str = query_str.replace(" ", "-")
    query_str = query_str.replace(",", "")

    return query_str



def get_members_json(chamber_str):

    req = requests.get(f"https://api.propublica.org/congress/v1/116/{chamber_str}/members.json", headers=headers)
    json_data = req.json()
    members = json_data["results"][0]["members"]

    extracted_members = extract_member_data(members)

    return extracted_members

def extract_member_data(members):

    chamber_members = []

    for member in members:

        if member["in_office"]:

            position=member["short_title"].replace('.','')
            position=position.lower()
            new_member = Member(id = member["id"], first_name=member["first_name"], last_name=member["last_name"], state_id=member["state"], party_id=member["party"], position_code=position)
            chamber_members.append(new_member)

    return chamber_members

