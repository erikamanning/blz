from app import db, headers
from models import Bill, SponsoredBill
import requests

def prune_summary(summary):

    if 'This bill' in summary:

        find_index = summary.find('This bill')
        
        lst = summary[find_index::]

        new_summary = str(lst)

        return new_summary
    
    else:

        return summary

def create_bill(bill_data):

    bill_data = bill_data['results'][0]

    if not bill_data["short_title"]:
        short_title = bill_data["title"]
    else:
        short_title=bill_data['short_title']

    new_bill = Bill(
            id = bill_data["bill_id"],
            bill_slug = bill_data["bill_slug"],
            congress = bill_data["congress"],
            bill = bill_data["bill"],
            bill_type = bill_data["bill_type"],
            number = bill_data["number"],
            title = bill_data["title"],
            short_title = short_title,
            sponsor_id = bill_data["sponsor_id"],
            congressdotgov_url = bill_data["congressdotgov_url"],
            introduced_date = bill_data["introduced_date"],
            active = bill_data["active"],
            last_vote = bill_data["last_vote"],
            house_passage = bill_data["house_passage"],
            senate_passage = bill_data["senate_passage"],
            enacted = bill_data["enacted"],
            vetoed = bill_data["vetoed"],
            primary_subject = bill_data["primary_subject"],
            committees = bill_data["committees"],
            committee_codes = bill_data["committee_codes"],
            latest_major_action_date = bill_data["latest_major_action_date"],
            latest_major_action = bill_data["latest_major_action"],
            house_passage_vote = bill_data["house_passage_vote"],
            senate_passage_vote = bill_data["senate_passage_vote"],
            summary = prune_summary(bill_data["summary"]),
            summary_short = bill_data["summary_short"]
    )

    # commit new bill
    db.session.add(new_bill)
    db.session.commit()

    # add sponsored bill
    add_sponsored_bill(new_bill)

def get_slugs(bill_data):

    slugs = []

    for bill in bill_data:

        slugs.append(bill["bill_slug"])

    return slugs

def get_bill_data(bill_slugs, congress):

    for slug in bill_slugs:

        req = requests.get(f'https://api.propublica.org/congress/v1/{congress}/bills/{slug}.json', headers=headers)
        json = req.json()
        create_bill(json)

def add_sponsored_bill(new_bill):

    new_sponsored_bill = SponsoredBill(bill_id=new_bill.id,sponsor_id=new_bill.sponsor_id)

    db.session.add(new_sponsored_bill)
    db.session.commit()
