from app import db, headers
from models import Bill, SponsoredBill
from fileread import FileRead
import requests
from get_bill_data_utility_functions import create_bill, get_slugs, get_bill_data


import pprint
pp = pprint.PrettyPrinter(indent=4)

# how to drop just this table
# Bill.__table__.drop(db.get_engine())
# Bill.__table__.create(db.get_engine())



def get_all_slugs(congress, chamber):

    all_slugs = []

    total = 20
    i = 0

    length = 20
    # print("Count: ", i)

    while length >= 20:

        # print(i)

        offset = total * i
        req = requests.get(f'https://api.propublica.org/congress/v1/{congress}/{chamber}/bills/introduced.json?offset={offset}', headers=headers)

        json = req.json()

        bill_data = json["results"][0]['bills']

        # pp.pprint(bill_data)

        slugs = get_slugs(bill_data)

        length = len(slugs)


        for slug in slugs:
            all_slugs.append(slug)

        i+=1

    
    return all_slugs

def get_some_slugs(congress, chamber, status, max_offset):

    all_slugs = []

    total = 20
    i = 0

    count=0

    length = 20
    # print("Count: ", i)

    while count <= max_offset:

        # print(i)

        offset = total * i
        req = requests.get(f'https://api.propublica.org/congress/v1/{congress}/{chamber}/bills/{status}.json?offset={offset}', headers=headers)

        json = req.json()

        bill_data = json["results"][0]['bills']

        # pp.pprint(bill_data)

        slugs = get_slugs(bill_data)

        # length = len(slugs)

        count +=1


        for slug in slugs:
            all_slugs.append(slug)

        i+=1

    
    return all_slugs

all_senate_slugs = get_some_slugs(116, "senate", 'introduced',2)
get_bill_data(all_senate_slugs, 116)


# all_senate_slugs = get_all_slugs(116, "senate")
# get_bill_data(all_senate_slugs, 116)

