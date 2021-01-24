from app import db, headers, CURRENT_SESSION
from models import Legislator, Bill, SponsoredBill
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

            if bill.primary_subject != bill_json['primary_subject'] or bill.latest_major_action != bill_json['latest_major_action'] or bill.latest_major_action_date != bill_json['latest_major_action_date']:

                bill.latest_major_action = bill_json['latest_major_action']
                bill.latest_major_action_date = bill_json['latest_major_action_date']
                bill.primary_subject = bill_json['primary_subject']
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

def get_bill_updates(chamber, session):

    got_all_updates = False

    offset_variable = 20

    count = 0

    while not got_all_updates:

        offset = offset_variable * count

        req = requests.get(f'https://api.propublica.org/congress/v1/{session}/{chamber}/bills/updated.json?offset={offset}',headers=headers)

        json = req.json()

        resp_data = json['results'][0]['bills']

        # pp.pprint(resp_data)

        got_all_updates = save_updates(resp_data, session)

        count+=1

