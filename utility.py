import requests
from models import Legislator, Bill, PolicyArea, SponsoredBill

from app import headers,db, CURRENT_SESSION
from datetime import date 
  
  
# Returns the current local date 
today = date.today() 
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



def get_legislators_json(chamber_str):

    req = requests.get(f"https://api.propublica.org/congress/v1/116/{chamber_str}/members.json", headers=headers)
    json_data = req.json()
    legislators = json_data["results"][0]["members"]

    extracted_legislators = extract_legislator_data(legislators)

    return extracted_legislators

def extract_legislator_data(legislators):

    chamber_legislators = []

    for legislator in legislators:

        if legislator["in_office"]:

            position=legislator["short_title"].replace('.','')
            position=position.lower()
            new_legislator = Legislator(id = legislator["id"], first_name=legislator["first_name"], last_name=legislator["last_name"], state_id=legislator["state"], party_id=legislator["party"], position_code=position)
            chamber_legislators.append(new_legislator)

    return chamber_legislators

