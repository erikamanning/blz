from unittest import TestCase
from app import app, db,headers, CURRENT_SESSION
import requests 
from flask import session
from models import Bill
from get_new_bills import get_new_bills
from get_bill_data_utility_functions import get_slugs

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class GetNewBillsTests(TestCase):

    def test_get_new_bills(self):

        # get 20 most recently updated bills
        req = requests.get(f'https://api.propublica.org/congress/v1/117/both/bills/introduced.json?offset=0',headers=headers)
        json = req.json()
        resp_data = json['results'][0]['bills']
        slugs = get_slugs(resp_data)

        current_bill_data = []

        # fill with dummy data
        for slug in slugs:

            bill = Bill.query.filter(Bill.congress == CURRENT_SESSION,Bill.bill_slug == slug).one_or_none()

            print('**********************')
            print(f'Current Bill {bill.bill_slug} data:')
            print(f'Date: {bill.introduced_date}')
            print('**********************')

            db.session.delete(bill)
            db.session.commit()

        for slug in slugs:

            bill = Bill.query.filter(Bill.congress == CURRENT_SESSION,Bill.bill_slug == slug).one_or_none()

            if bill:

                print(f'BILL {slug} WAS NOT DELETED')

            else:

                print(f'BILL {slug} DOES NOT EXIST')


        get_new_bills(117, "both", 'introduced')


        for slug in slugs:

            bill = Bill.query.filter(Bill.congress == CURRENT_SESSION,Bill.bill_slug == slug).one_or_none()

            if bill:

                print(f'BILL {slug} HAS BEEN ADDED')

            else:

                print(f'BILL {slug} DOES NOT EXIST')

            self.assertTrue(bill)

# most_recent_bill_date = '2021-01-15'

# most_recent_bills = Bill.query.filter(Bill.introduced_date==most_recent_bill_date).all()
# print(most_recent_bills)

# for bill in most_recent_bills:

#     print(f'Bill: {bill.id}, Date: {bill.introduced_date}')
#     db.session.delete(bill)


# db.session.commit()

# #  check bills deleted
# recent_bill_check = Bill.query.filter(Bill.introduced_date==most_recent_bill_date).all()

# if recent_bill_check:

#     for bill in recent_bill_check:

#         print('New Bills Found!!')
#         print(f'Bill: {bill.id}, Date: {bill.introduced_date}')

# else:

#     print('No bills found for ', most_recent_bill_date)


# print('******************************')
# print('Getting new bills: ')
# print('******************************')


# get_new_bills(117,"both", "introduced")

# recent_bill_check = Bill.query.filter(Bill.introduced_date==most_recent_bill_date).all()

# if recent_bill_check:

#     print('New bills found!')
#     for bill in recent_bill_check:

#         print(f'Bill: {bill.id}, Date: {bill.introduced_date}')

# else:

#     print('No bills found for ', most_recent_bill_date)
