from app import db, headers, CURRENT_CONGRESS_SESSION
from models import Bill
import requests
from sqlalchemy import and_, or_
from get_app_data.get_bill_data_utility_functions import create_bill, get_slugs, get_bill_data


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

            else:

                # reached the end of updates
                return True
    
    # 20 updates were made, moving on to next section
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

        got_all_updates = save_updates(resp_data, session)

        count+=1


get_bill_updates('both',CURRENT_CONGRESS_SESSION)