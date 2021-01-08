from app import db, headers, CURRENT_SESSION
from models import Member, Bill, SponsoredBill
import requests
from sqlalchemy import and_, or_
from get_bill_data_utility_functions import create_bill, get_slugs, get_bill_data

import pprint
pp = pprint.PrettyPrinter(indent=4)

print('**********************************')
print('STARTING UPDATE PROCESS')
print('**********************************')


def save_updates(updates_json, session):

    for bill_json in updates_json:

        bill = Bill.query.filter(Bill.congress==session, Bill.bill_slug == bill_json['bill_slug']).one_or_none()

        if bill:

            if bill.latest_major_action != bill_json['latest_major_action'] or bill.latest_major_action_date != bill_json['latest_major_action_date']:

                bill.latest_major_action = bill_json['latest_major_action']
                bill.latest_major_action_date = bill_json['latest_major_action_date']
                db.session.add(bill)
                db.session.commit()
                print('**********************************')
                print(f'BILL {bill.bill_slug} UPDATED')
                print('**********************************')

            else:

                # reached the end of updates

                print('**********************************')
                print('NO MORE UPDATES')
                print('**********************************')

                return True
    
    # 20 updates were made, moving on to next section
    print('**********************************')
    print('ROUND OF UPDATES COMPLETE, MOVING TO NEXT ROUND')
    print('**********************************')
    return False
    
    # else:

    #     print('**********************************')
    #     print('NO UPDATES AVAILBLE')
    #     print('**********************************')
    #     return True

def get_bill_updates(chamber, session):

    got_all_updates = False

    offset_variable = 20

    count = 0

    while not got_all_updates:

        offset = offset_variable * count

        req = requests.get(f'https://api.propublica.org/congress/v1/{session}/{chamber}/bills/updated.json?offset={offset}',headers=headers)

        json = req.json()

        resp_data = json['results'][0]['bills']

        pp.pprint(resp_data)

        got_all_updates = save_updates(resp_data, session)

        count+=1


# get updates for bills/ stop while last updated stamp is not same as bill we are currently on

    # get most recent last updated timestamp/ query all bills in order of last updated limit 1

    # loop and get updated bill data until there are no bills newer than the last updated timestamp

    # commit sponsored bills

    # check that both of these are the same

        #   "latest_major_action_date": "2020-12-31",
        #   "latest_major_action": "Presented to President."


# will need to write loop later to go through all sessions since the api
# does not grab updates without a session specified
get_bill_updates('senate',CURRENT_SESSION)