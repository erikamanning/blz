from unittest import TestCase
from app import app, db
from flask import session
from models import User, PolicyArea, Party, State, Legislator
  
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False


class TestBillSearch(TestCase):

    @classmethod
    def setUpClass(cls):


        # add dummy data

        # add dummy parties
        cls.add_dummy_party('dummy_code1', 'RabbitParty')
        cls.add_dummy_party('dummy_code2', 'DuckParty')
        cls.add_dummy_party('dummy_code3', 'DeerParty')

        # # add dummy states
        cls.add_dummy_state('dummy_acronym1', 'Sillanois')
        cls.add_dummy_state('dummy_acronym2', 'Nexas')
        cls.add_dummy_state('dummy_acronym3', 'Yorknew')

        # # add dummy legislators
        cls.add_dummy_legislator('dummy_00000001', 'aaaa', 'dummy_acronym1', 'Sen.','dummy_code1')
        cls.add_dummy_legislator('dummy_00000002', 'aaab', 'dummy_acronym3', 'Sen.','dummy_code2')
        cls.add_dummy_legislator('dummy_00000003', 'aaac', 'dummy_acronym2', 'R.C.','dummy_code3')
        cls.add_dummy_legislator('dummy_00000004', 'aaad', 'dummy_acronym1', 'Del.','dummy_code2')

        print('Setup')
    

    @classmethod
    def tearDownClass(cls):

        # remove dummy data
        cls.remove_dummy_legislators()
        cls.remove_dummy_parties()
        cls.remove_dummy_states()


        print("Teardown")

    @classmethod
    def add_dummy_party(cls,party_code, party_name):

        dummy_party = Party(code =party_code, name= party_name)
        db.session.add(dummy_party)
        db.session.commit()

    @classmethod
    def add_dummy_state(cls,state_acronym, state_name):

        dummy_state = State( acronym=state_acronym, name= state_name)
        db.session.add(dummy_state)
        db.session.commit()

    @classmethod
    def add_dummy_legislator(cls, legislator_id, last_name, state, position, party):
        new_legislator = Legislator(
            id=legislator_id,
            first_name='DUMMY_VAL', 
            last_name=last_name, 
            image= 'DUMMY_VAL', 
            state_id=state,
            party_id=party,
            position_code=position, 
            website = 'DUMMY_VAL',
            in_office=True,
            twitter_account = 'DUMMY_VAL',
            facebook_account ='DUMMY_VAL',
            youtube_account ='DUMMY_VAL',
            office_address = 'DUMMY_VAL',
            phone = 'DUMMY_VAL'
        )

        db.session.add(new_legislator)
        db.session.commit()

    @classmethod
    def remove_dummy_legislators(cls):

        for dummy_legislator in Legislator.query.filter(Legislator.id.contains('dummy')).all():

            db.session.delete(dummy_legislator)
            db.session.commit()

    @classmethod
    def remove_dummy_parties(cls):

        for dummy_party in Party.query.filter(Party.code.contains('dummy')).all():

            db.session.delete(dummy_party)
            db.session.commit()

    @classmethod
    def remove_dummy_states(cls):

        for dummy_state in State.query.filter(State.acronym.contains('dummy')).all():

            db.session.delete(dummy_state)
            db.session.commit()


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
                'chamber' : 'Sen.'
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


