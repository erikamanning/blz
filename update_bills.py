from app import db, headers
from models import Member, Bill, SponsoredBill
import requests
from sqlalchemy import and_
from get_bill_data_utility_functions import create_bill, get_slugs, get_bill_data

# Notes for improvements
# turn reusuable functions here and in get_bills module to a separate file 
# so they can be called in both, cannot do it now with current setip

# update bills
# update Sponsored bills/ new sponsored bills should show up for members
# update members?


# checks slugs to see if not caught up yet, returns boolean status 
def check_slugs(slugs, current_session):

    for slug in slugs:

        if Bill.query.filter(and_(Bill.bill_slug == slug, Bill.congress == current_session)).one_or_none():

            caught_up_index = slugs.index(slug)
            trimmed_slugs_list = []
            trimmed_slugs_list[0:caught_up_index]

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

        checked_slugs = check_slugs(slugs, current_session)

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

# get updates for bills/ stop while last updated stamp is not same as bill we are currently on

    # get most recent last updated timestamp/ query all bills in order of last updated limit 1

    # loop and get updated bill data until there are no bills newer than the last updated timestamp

    # commit sponsored bills

    # check that both of these are the same

        #   "latest_major_action_date": "2020-12-31",
        #   "latest_major_action": "Presented to President."



get_new_bills('116', "senate", 'introduced')
