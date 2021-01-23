from unittest import TestCase
from app import app, db, CURRENT_SESSION
from flask import session
from models import User, PolicyArea, Bill
from datetime import date 
from get_bill_data_utility_functions import handle_policy_area, add_sponsored_bill
  
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

TODAY = date.today()

class TestBillSearch(TestCase):

    @classmethod
    def setUpClass(cls):

        # add dummy bills
        cls.policy_area_str_1 = 'dummy Cartoon Dog Regulations'
        cls.policy_area_str_2 = 'dummy Anti Rainwater Laws'

        cls.add_dummy_bill('a',cls.policy_area_str_1,TODAY, TODAY)
        cls.add_dummy_bill('b',cls.policy_area_str_2 ,'2021-01-04', '2021-01-04')
        cls.add_dummy_bill('c',cls.policy_area_str_2 ,'2021-01-05', '2021-01-05')

        cls.policy_area_1 = PolicyArea.query.filter(PolicyArea.name==cls.policy_area_str_1).one_or_none()
        cls.policy_area_2 = PolicyArea.query.filter(PolicyArea.name==cls.policy_area_str_2).one_or_none()

        print('Setup')
    

    @classmethod
    def tearDownClass(cls):

        cls.remove_dummy_bills()
        cls.remove_dummy_policy_areas()

        print("Teardown")

    @classmethod
    def add_dummy_bill(cls, bill_id, policy_area,introduced_date, latest_major_action_date ):

        new_bill = Bill(
                id = f'dummy_bill_{bill_id}',
                bill_slug = 'dummy_slug',
                congress = CURRENT_SESSION,        
                bill = 'dummy_bill',            
                bill_type = 'dummy_bill_type',
                number = 'dummy_number',
                title = 'dummy_title',
                short_title = 'dummy_short_title',
                sponsor_id = 'B001285',
                congressdotgov_url = 'dummy_congressdotgov_url',
                introduced_date = introduced_date,
                active = False,
                last_vote = 'dummy_last_vote',
                house_passage = 'dummy_house_passage',
                senate_passage = 'dummy_senate_passage',
                enacted = 'dummy_enacted',
                vetoed = 'dummy_vetoed',
                primary_subject = policy_area,
                committees = 'dummy_committees',
                committee_codes = 'dummy_committee_codes',
                latest_major_action_date = latest_major_action_date,
                latest_major_action = 'dummy_latest_major_action',
                house_passage_vote = 'dummy_house_passage_vote',
                senate_passage_vote = 'dummy_senate_passage_vote',
                summary = 'dummy_summary',
                summary_short = 'dummy_summary_short'
        )

        # commit new bill
        db.session.add(new_bill)
        db.session.commit()

        handle_policy_area(new_bill.primary_subject)
        add_sponsored_bill(new_bill)

        return new_bill

    @classmethod
    def remove_dummy_bills(cls):

        dummy_bills = Bill.query.filter(Bill.id.contains('dummy_bill_')).all()

        for bill in dummy_bills:

            db.session.delete(bill)
            db.session.commit()

    @classmethod
    def remove_dummy_policy_areas(cls):

        dummy_policy_areas = PolicyArea.query.filter(PolicyArea.name.contains('dummy')).all()

        for policy_area in dummy_policy_areas:

            db.session.delete(policy_area)
            db.session.commit()

    # test if correct bills load with no data passed to form
    def test_bill_search_any_subject(self):
        with app.test_client() as client:
            d= {
                'policy_area' : '',
                'start_date' : '',
                'end_date' : ''
            }
            resp = client.get('/bills', data=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('dummy_bill_a', html)

    # test if correct bills load with a specific subject passed to form
    def test_bill_search_specific_subject_a(self):
        with app.test_client() as client:
            d= {
                'policy_area' : TestBillSearch.policy_area_1.id,
                'start_date' : '',
                'end_date' : ''
            }
            resp = client.get(f'/bills',query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('dummy_bill_a', html)
            self.assertNotIn('dummy_bill_b', html)

    #test if correct bills load with a specific subject passed to form
    def test_bill_search_specific_subject_b(self):
        with app.test_client() as client:
            d= {
                'policy_area' : TestBillSearch.policy_area_2.id,
                'start_date' : '',
                'end_date' : ''
            }
            resp = client.get(f'/bills',query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('dummy_bill_b', html)
            self.assertIn('dummy_bill_c', html)
            self.assertNotIn('dummy_bill_a', html)

    #test if correct bills load with a specific subject & date passed to form
    def test_bill_search_specific_subject_date(self):
        with app.test_client() as client:
            d= {
                'policy_area' : TestBillSearch.policy_area_2.id,
                'start_date' : '2021-01-04',
                'end_date' : '2021-01-04'
            }
            resp = client.get(f'/bills',query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('dummy_bill_b', html)
            self.assertNotIn('dummy_bill_c', html)

    #test if correct bills load with start date only passed to form
    def test_bill_search_only_start_date(self):
        with app.test_client() as client:
            d= {
                'policy_area' : '',
                'start_date' : TODAY,
                'end_date' : ''
            }
            resp = client.get(f'/bills',query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('dummy_bill_a', html)
            self.assertNotIn('dummy_bill_b', html)
            self.assertNotIn('dummy_bill_c', html)

    #test if correct bills load with end date only passed to form
    def test_bill_search_only_end_date(self):
        with app.test_client() as client:
            d= {
                'policy_area' : '',
                'start_date' : '',
                'end_date' : TODAY
            }
            resp = client.get(f'/bills',query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('dummy_bill_a', html)
            self.assertNotIn('dummy_bill_b', html)
            self.assertNotIn('dummy_bill_c', html)

    #test if correct bills load with start & end date only passed to form
    def test_bill_search_only_full_date(self):
        with app.test_client() as client:
            d= {
                'policy_area' : '',
                'start_date' : TODAY,
                'end_date' : TODAY
            }
            resp = client.get(f'/bills',query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('dummy_bill_a', html)
            self.assertNotIn('dummy_bill_b', html)
            self.assertNotIn('dummy_bill_c', html)


