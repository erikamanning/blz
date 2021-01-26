from unittest import TestCase
from app import app, db
from flask import session
from models import User, Bill, BillFollows

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class UserTests(TestCase):

    @classmethod
    def setUpClass(cls):
    
        # add test user
        cls.test_user_a = User.register(username='test_user_a', password='test123', email='testuser_a@email.com', state_id='NV')
        cls.test_user_b = User.register(username='test_user_b', password='test123', email='testuser_b@email.com', state_id='NV')
        db.session.add_all([cls.test_user_a,cls.test_user_b])
        db.session.commit()

    @classmethod
    def tearDownClass(cls):

        # delete test users
        db.session.delete(cls.test_user_a)
        db.session.delete(cls.test_user_b)
        db.session.commit()

    def setUp(self):
        # create test user to delete
        self.test_user_c = User.register(username='test_user_c', password='test123', email='testuser_c@email.com', state_id='NV')
        db.session.add(self.test_user_c)
        db.session.commit()

    def tearDown(self):
        db.session.delete(self.test_user_c)
        db.session.commit()

    def test_register_new_user(self):

        test_user_d = User.register(username='test_user_d', password='test123', email='testuser_d@email.com', state_id='NV')
        self.assertTrue(test_user_d)

    def test_register_new_user_no_state(self):

        test_user_d = User.register(username='test_user_d', password='test123', email='testuser_d@email.com')
        self.assertTrue(test_user_d)

    def test_authenticate_user(self):

        authenticated = User.authenticate(UserTests.test_user_a.username, password='test123' )
        self.assertTrue(authenticated)

    def test_user_not_authenticated(self): 

        authenticated = User.authenticate(UserTests.test_user_a.username, password='abcdefg' )
        self.assertFalse(authenticated)

    def test_user_follows(self):

        # create test bill follows
        bill_ids = db.session.query(Bill.id).limit(3).all()
        for bill_id in bill_ids:
            new_bill_follow = BillFollows(bill_id=bill_id[0],user_id=self.test_user_c.id)
            db.session.add(new_bill_follow)

        db.session.commit()

        follow_ids = []

        for followed_bill in self.test_user_c.followed_bills:

            follow_ids.append(followed_bill.id)

        # check follows
        for bill_id in bill_ids:
            self.assertTrue(bill_id[0] in follow_ids)

