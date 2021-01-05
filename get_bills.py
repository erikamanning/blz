from app import db, headers
from models import Bill, SponsoredBill
from fileread import FileRead
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)

# db.drop_all()
# db.create_all()

# Bill.__table__.drop(db.get_engine())
# Bill.__table__.create(db.get_engine())


bill_data = requests.get('https://api.propublica.org/congress/v1/116/senate/bills/introduced.json?offset=40', headers = headers)

bill_data = bill_data.json()
bill_data = bill_data["results"][0]['bills']

def get_slugs(bills):

    slugs = []

    for bill in bills:

        slugs.append(bill["bill_slug"])

    return slugs

def create_bill(bill_data):

    bill_data = bill_data['results'][0]

    new_bill = Bill(
            id = bill_data["bill_id"],
            bill_slug = bill_data["bill_slug"],
            congress = bill_data["congress"],
            bill = bill_data["bill"],
            bill_type = bill_data["bill_type"],
            number = bill_data["number"],
            title = bill_data["title"],
            short_title = bill_data["short_title"],
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
            summary = bill_data["summary"],
            summary_short = bill_data["summary_short"]
    )
    db.session.add(new_bill)
    db.session.commit()

    # make its own function
    # find out if this is the best time to do this
    # it may not be optimized
    new_sponsored_bill = SponsoredBill(bill_id=new_bill.id,sponsor_id=new_bill.sponsor_id)
    db.session.add(new_sponsored_bill)
    db.session.commit()


def get_bill_data(bill_slugs, congress):

    for slug in bill_slugs:

        req = requests.get(f'https://api.propublica.org/congress/v1/{congress}/bills/{slug}.json', headers=headers)
        json = req.json()
        create_bill(json)

def get_all_slugs(congress, chamber):

    all_slugs = []

    total = 20
    i = 0

    length = 20
    print("Count: ", i)

    while length >= 20:

        print(i)

        offset = total * i
        req = requests.get(f'https://api.propublica.org/congress/v1/{congress}/{chamber}/bills/introduced.json?offset={offset}', headers=headers)

        json = req.json()

        bill_data = json["results"][0]['bills']

        pp.pprint(bill_data)

        slugs = get_slugs(bill_data)

        length = len(slugs)


        for slug in slugs:
            all_slugs.append(slug)

        i+=1

    
    return all_slugs

def get_some_slugs(congress, chamber, max_offset):

    all_slugs = []

    total = 20
    i = 0

    count=1

    length = 20
    print("Count: ", i)

    while count <= max_offset:

        print(i)

        offset = total * i
        req = requests.get(f'https://api.propublica.org/congress/v1/{congress}/{chamber}/bills/introduced.json?offset={offset}', headers=headers)

        json = req.json()

        bill_data = json["results"][0]['bills']

        pp.pprint(bill_data)

        slugs = get_slugs(bill_data)

        # length = len(slugs)

        count +=1


        for slug in slugs:
            all_slugs.append(slug)

        i+=1

    
    return all_slugs

all_senate_slugs = get_some_slugs(116, "senate",4)
get_bill_data(all_senate_slugs, 116)


# all_senate_slugs = get_all_slugs(116, "senate")
# get_bill_data(all_senate_slugs, 116)

