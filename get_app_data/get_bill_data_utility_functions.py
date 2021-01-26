from app import db, headers
from models import Bill, SponsoredBill,PolicyArea
import requests

def create_bill(bill_data):

    bill_data = bill_data['results'][0]

    if bill_data.get("short_title",False):
        short_title=bill_data['short_title']
    else:
        short_title = bill_data["title"]

    if bill_data.get("primary_subject",False):
        primary_subject = bill_data['primary_subject']
    else:
        primary_subject='No Primary Subject'

    new_bill = Bill(
            id = bill_data["bill_id"],
            bill_slug = bill_data["bill_slug"],
            congress = bill_data["congress"],
            # bill = bill_data["bill"],
            title = bill_data["title"],
            short_title = short_title,
            sponsor_id = bill_data["sponsor_id"],
            congressdotgov_url = bill_data["congressdotgov_url"],
            introduced_date = bill_data["introduced_date"],
            primary_subject = primary_subject,
            latest_major_action_date = bill_data["latest_major_action_date"],
            latest_major_action = bill_data["latest_major_action"],
            summary = bill_data["summary"],
            summary_short = bill_data["summary_short"]
    )

    # commit new bill
    db.session.add(new_bill)
    db.session.commit()

    # handle policy area
    handle_policy_area(new_bill.primary_subject)

    # add sponsored bill
    add_sponsored_bill(new_bill)



def get_slugs(bill_data):

    slugs = []

    for bill in bill_data:

        slugs.append(bill["bill_slug"])

    return slugs

def get_bill_data(bill_slugs, congress):

    i=0

    for slug in bill_slugs:

        req = requests.get(f'https://api.propublica.org/congress/v1/{congress}/bills/{slug}.json', headers=headers)
        json = req.json()
        i+=1
        print('Creating bill: ', i)
        create_bill(json)


def add_sponsored_bill(new_bill):

    new_sponsored_bill = SponsoredBill(bill_id=new_bill.id,sponsor_id=new_bill.sponsor_id)

    db.session.add(new_sponsored_bill)
    db.session.commit()

def handle_policy_area(policy_area):

    if not PolicyArea.query.filter(PolicyArea.name == policy_area).one_or_none():

        new_policy_area = PolicyArea(name=policy_area)
        db.session.add(new_policy_area)
        db.session.commit()
