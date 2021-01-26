from app import db, headers, CURRENT_CONGRESS_SESSION
from models import Bill
import requests
from sqlalchemy import and_
from get_bill_data_utility_functions import create_bill, get_slugs, get_bill_data

# checks slugs to see if not caught up yet, returns boolean status 
def check_slugs(slugs, current_session):

    for slug in slugs:

        if Bill.query.filter(and_(Bill.bill_slug == slug, Bill.congress == current_session)).one_or_none():

            caught_up_index = slugs.index(slug)
            trimmed_slugs_list = slugs[0:caught_up_index]

            return trimmed_slugs_list

    return slugs

def get_new_bill_slugs(current_session, chamber, status):

    all_new_bill_slugs = []

    caught_up = False

    offset_variable = 20

    count = 0

    while not caught_up:

        offset = offset_variable * count

        req = requests.get(f'https://api.propublica.org/congress/v1/{current_session}/{chamber}/bills/{status}.json?offset={offset}',headers=headers)

        json = req.json()

        resp_data = json['results'][0]['bills']

        slugs = get_slugs(resp_data)

        print('Slugs: ', slugs)

        checked_slugs = check_slugs(slugs, current_session)

        print('Checked Slugs: ', checked_slugs)

        for slug in checked_slugs:

            all_new_bill_slugs.append(slug)

        if len(checked_slugs) < 20:

            caught_up = True

        else:

            count+=1

    return all_new_bill_slugs


def get_new_bills(current_session, chamber, status):

    new_bill_slugs = get_new_bill_slugs(current_session, chamber, status)
    get_bill_data(new_bill_slugs, current_session)


get_new_bills(CURRENT_CONGRESS_SESSION, "both", 'introduced')
