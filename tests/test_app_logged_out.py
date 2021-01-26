from unittest import TestCase
from app import app, db
from flask import session
from models import User

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

class ViewsLoggedOutTests(TestCase):

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

        print("Teardown")

    # test if home page loads
    def test_root_route(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-1 text-center pt-5">Welcome to BLZ</h1>', html)

    # test if bill browse page loads
    def test_bills_route(self):
        with app.test_client() as client:
            resp = client.get('/bills')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p class="lead text-center mb-5 mt-3">A place to view and follow bills from the 117th (current) Session of Congress.</p>', html)

    # test if legislator browse page loads
    def test_legislator_route(self):
        with app.test_client() as client:
            resp = client.get('/legislators')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p class="lead text-center mt-3">A place to view Legislators and the bills they have sponsored lately. </p', html)

    # test if login page loads
    def test_login_route(self):
        with app.test_client() as client:
            resp = client.get('/login')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="text-center mt-5">Login</h1>', html)

    # test if signup page loads
    def test_signup_route(self):
        with app.test_client() as client:
            resp = client.get('/signup')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="text-center mt-5">Sign Up</h1>', html)

    # test if view dashboard screen does not load when not logged in and user is rerouted
    def test_view_dashboard_route_lo(self):
        with app.test_client() as client:
            resp = client.get('/dashboard',follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must be logged in to do that!', html)

    # test if view profile screen does not load when not logged in and user is rerouted
    def test_view_profile_route_lo(self):
        with app.test_client() as client:
            resp = client.get('/profile',follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must be logged in to do that!', html)

    # test if edit profile screen does not load when not logged in and user is rerouted
    def test_edit_profile_route_lo(self):
        with app.test_client() as client:
            resp = client.get('/profile/edit',follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must be logged in to do that!', html)

    # test if delete profile screen does not load when not logged in and user is rerouted
    def test_delete_profile_route_lo(self):
        with app.test_client() as client:
            resp = client.get('/profile/delete',follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must be logged in to do that!', html)

    # test logout denial when already logged out in another tab
    def test_logout_lo(self):
        with app.test_client() as client:

            resp = client.post("/logout", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('No user currently logged in!', html)

    # test if legislator page loads
    def test_legislator_view(self):
        with app.test_client() as client:
            resp = client.get('/legislator/L000577')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("View Sponsored Bills", html)

    # test if bill page loads
    def test_bill_view(self):
        with app.test_client() as client:
            resp = client.get('/bill/hr354-117')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('View Full Bill at', html)

    # test if duplicate username rejected on signup
    def test_signup_duplicate_username_route(self):
        with app.test_client() as client:
            d= {
                'username' : 'test_user_a',
                'password' : 'test123', 
                'email' : '123456testuser_a@email.com', 
                'state' : 'NV'
            }
            resp = client.post('/signup', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('That username is already taken! Please choose another.', html)
    
    # test if duplicate email rejected on signup
    def test_signup_duplicate_email_route(self):
        with app.test_client() as client:
            d= {
                'username' : 'test_user_10',
                'password' : 'test123', 
                'email' : 'testuser_b@email.com', 
                'state' : 'NV'
            }
            resp = client.post('/signup', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('There is already an account with that email. Please use another email.', html)


   