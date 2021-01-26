from unittest import TestCase
from app import app, db
from flask import session
from models import Party, State, Legislator
from tests.dummy_data_generators import add_dummy_party, add_dummy_state, add_dummy_legislator, remove_dummy_legislators, remove_dummy_parties, remove_dummy_states

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False


class TestBillSearch(TestCase):

    @classmethod
    def setUpClass(cls):

        # add dummy parties
        add_dummy_party('dummy_code1', 'RabbitParty')
        add_dummy_party('dummy_code2', 'DuckParty')
        add_dummy_party('dummy_code3', 'DeerParty')

        #add dummy states
        add_dummy_state('dummy_acronym1', 'Sillanois')
        add_dummy_state('dummy_acronym2', 'Nexas')
        add_dummy_state('dummy_acronym3', 'Yorkne')

        # add dummy legislators
        add_dummy_legislator('dummy_00000001', 'aaaa', 'dummy_acronym1', 'Sen.','dummy_code1')
        add_dummy_legislator('dummy_00000002', 'aaab', 'dummy_acronym3', 'Sen.','dummy_code2')
        add_dummy_legislator('dummy_00000003', 'aaac', 'dummy_acronym2', 'R.C.','dummy_code3')
        add_dummy_legislator('dummy_00000004', 'aaad', 'dummy_acronym1', 'Del.','dummy_code2')

        print('Setup')
    
    @classmethod
    def tearDownClass(cls):

        # remove dummy data
        remove_dummy_legislators()
        remove_dummy_parties()
        remove_dummy_states()

        print("Teardown")

    # test if expected legislators load with no data passed through form
    def test_legislators_search_no_specs(self):
        with app.test_client() as client:

            resp = client.get('/legislators')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('aaaa', html)
            self.assertIn('aaab', html)
            self.assertIn('aaac', html)
            self.assertIn('aaad', html)

    # test if expected legislators load with party passed through only
    def test_legislators_search_party_only(self):
        with app.test_client() as client:
            d= {
                'party' : 'dummy_code3'
            }
            resp = client.get('/legislators', query_string=d )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('aaac', html)
            self.assertNotIn('aaaa', html)
            self.assertNotIn('aaab', html)
            self.assertNotIn('aaad', html)


    # test if expected legislators load with state passed through only
    def test_legislators_search_state_only(self):
        with app.test_client() as client:
            d= {
                'state' : 'dummy_acronym2'
            }
            resp = client.get('/legislators', query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('aaac', html)
            self.assertNotIn('aaaa', html)
            self.assertNotIn('aaab', html)
            self.assertNotIn('aaad', html)

    # test if expected legislators load with position passed through only
    def test_legislators_search_position_only(self):
        with app.test_client() as client:
            d= {
                'position' : 'Sen.'
            }
            resp = client.get('/legislators', query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('aaaa', html)
            self.assertIn('aaab', html)
            self.assertNotIn('aaac', html)
            self.assertNotIn('aaad', html)


    # test if expected legislators load with only party & state passed through
    def test_legislators_search_party_state(self):
        with app.test_client() as client:
            d= {
                'party':'dummy_code2',
                'state':'dummy_acronym1'
            }
            resp = client.get('/legislators', query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('aaad', html)
            self.assertNotIn('aaab', html)
            self.assertNotIn('aaac', html)
            self.assertNotIn('aaaa', html)

    # test if expected legislators load with only party & position passed through
    def test_legislators_search_party_position(self):
        with app.test_client() as client:
            d= {
                'party':'dummy_code1',
                'position':'Sen.'
            }
            resp = client.get('/legislators', query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('aaaa', html)
            self.assertNotIn('aaab', html)
            self.assertNotIn('aaac', html)
            self.assertNotIn('aaad', html)

    # test if expected legislators load with only party & position passed through
    def test_legislators_search_state_position(self):
        with app.test_client() as client:
            d= {
                'state':'dummy_acronym3',
                'position':'Sen.'
            }
            resp = client.get('/legislators', query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('aaab', html)
            self.assertNotIn('aaaa', html)
            self.assertNotIn('aaac', html)
            self.assertNotIn('aaad', html)


        # test if expected legislators load with state, party, & position passed through
    def test_legislators_search_state_party_position(self):
        with app.test_client() as client:
            d= {
                'state':'dummy_acronym3',
                'position':'Sen.',
                'party' : 'dummy_code2'
            }
            resp = client.get('/legislators', query_string=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('aaab', html)
            self.assertNotIn('aaaa', html)
            self.assertNotIn('aaac', html)
            self.assertNotIn('aaad', html)


