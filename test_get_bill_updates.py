from unittest import TestCase
from app import app, db,headers, CURRENT_SESSION
import requests 
from flask import session
from models import User, Bill
from get_bill_updates import get_bill_updates
from get_bill_data_utility_functions import get_slugs

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class UpdateBillsTests(TestCase):

    def test_get_bill_updates_date_detail(self):

        # get 20 most recently updated bills
        req = requests.get(f'https://api.propublica.org/congress/v1/117/both/bills/updated.json?offset=0',headers=headers)
        json = req.json()
        resp_data = json['results'][0]['bills']
        slugs = get_slugs(resp_data)

        current_bill_data = []

        # fill with dummy data
        for slug in slugs:

            bill = Bill.query.filter(Bill.congress == CURRENT_SESSION,Bill.bill_slug == slug).one_or_none()

            print('**********************')
            print(f'Current Bill {bill.bill_slug} data:')
            print('**********************')
            print(f'Date: {bill.latest_major_action_date}')
            print(f'Update: {bill.latest_major_action}')

            current_bill_data.append( 
                {
                    'bill_slug':bill.bill_slug, 
                    'lma_d': bill.latest_major_action_date,
                    'lma': bill.latest_major_action
                }
            )

            bill.latest_major_action = '99999999999999999999999999999999999999999'
            bill.latest_major_action_date = '0000-00-00'

            db.session.add(bill)
            db.session.commit()

            print('**********************')
            print(f'After Dummy Data. Bill {bill.bill_slug}:')
            print('**********************')
            print(f'Date: {bill.latest_major_action_date}')
            print(f'Update: {bill.latest_major_action}')


        # Update

        get_bill_updates('both',CURRENT_SESSION)

        for slug in slugs:

            bill = Bill.query.filter(Bill.congress == CURRENT_SESSION,Bill.bill_slug == slug).one_or_none()

            print('**********************')
            print(f'After Updates. Bill Data for {bill.bill_slug}:')
            print('**********************')
            print(f'Date: {bill.latest_major_action_date}')
            print(f'Update: {bill.latest_major_action}')


        for current_bill in current_bill_data:

            bill = Bill.query.filter(Bill.congress == CURRENT_SESSION,Bill.bill_slug == current_bill['bill_slug']).one_or_none()

            self.assertEqual(current_bill['lma_d'], bill.latest_major_action_date)
            self.assertEqual(current_bill['lma'], bill.latest_major_action)
            
    def test_get_same_day_updates(self):

        # get 20 most recently updated bills
        req = requests.get(f'https://api.propublica.org/congress/v1/117/both/bills/updated.json?offset=0',headers=headers)
        json = req.json()
        resp_data = json['results'][0]['bills']
        slugs = get_slugs(resp_data)

        current_bill_data = []

        # fill with dummy data
        for slug in slugs:

            bill = Bill.query.filter(Bill.congress == CURRENT_SESSION,Bill.bill_slug == slug).one_or_none()

            print('**********************')
            print(f'Current Bill {bill.bill_slug} data:')
            print('**********************')
            print(f'Date: {bill.latest_major_action_date}')
            print(f'Update: {bill.latest_major_action}')

            current_bill_data.append( 
                {
                    'bill_slug':bill.bill_slug, 
                    'lma_d': bill.latest_major_action_date,
                    'lma': bill.latest_major_action
                }
            )

            bill.latest_major_action = '99999999999999999999999999999999999999999'

            db.session.add(bill)
            db.session.commit()

            print('**********************')
            print(f'After Dummy Data. Bill {bill.bill_slug}:')
            print('**********************')
            print(f'Date: {bill.latest_major_action_date}')
            print(f'Update: {bill.latest_major_action}')


        # Update

        get_bill_updates('both',CURRENT_SESSION)

        for slug in slugs:

            bill = Bill.query.filter(Bill.congress == CURRENT_SESSION,Bill.bill_slug == slug).one_or_none()

            print('**********************')
            print(f'After Updates. Bill Data for {bill.bill_slug}:')
            print('**********************')
            print(f'Date: {bill.latest_major_action_date}')
            print(f'Update: {bill.latest_major_action}')


        for current_bill in current_bill_data:

            bill = Bill.query.filter(Bill.congress == CURRENT_SESSION,Bill.bill_slug == current_bill['bill_slug']).one_or_none()

            self.assertEqual(current_bill['lma_d'], bill.latest_major_action_date)
            self.assertEqual(current_bill['lma'], bill.latest_major_action)
            

# most_recent_update_date = '2021-01-15'

# most_recently_updated_bills = Bill.query.filter(Bill.latest_major_action_date==most_recent_update_date).all()
# print(most_recently_updated_bills)

# for bill in most_recently_updated_bills:

#     print(f'Bill: {bill.id}, Date: {bill.latest_major_action_date}')
#     bill.latest_major_action = 'nyehehehehe'
#     bill.latest_major_action_date = '99-99-99'

# db.session.add_all(most_recently_updated_bills)
# db.session.commit()

# #  check bills deleted
# recent_bill_check = Bill.query.filter(Bill.latest_major_action_date=='99-99-99').all()



# for bill in recent_bill_check:

#     print(f'Bill: {bill.id}, Date: {bill.latest_major_action_date}')
#     print(f'Date: {bill.latest_major_action_date}')
#     print(f'Update: {bill.latest_major_action}')


# print('******************************')
# print('Getting bill updates... ')
# print('******************************')


# get_bill_updates("both",117 )

# recent_bill_check = Bill.query.filter(Bill.latest_major_action_date==most_recent_update_date).all()


# print('******************************')
# print('New Bills Found!!')
# print('******************************')


# for bill in recent_bill_check:

#     print(f'Bill: {bill.id}, Date: {bill.latest_major_action_date}')
#     print(f'Date: {bill.latest_major_action_date}')
#     print(f'Update: {bill.latest_major_action}')
