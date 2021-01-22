from unittest import TestCase
from app import app, db
from flask import session
from models import User

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



class ViewsLoggedInTests(TestCase):
    app.config['WTF_CSRF_ENABLED'] = False

    @classmethod
    def setUpClass(cls):

        # add test user
        cls.test_user = User.register(username='test_user3', password='test123', email='test3@email.com', state_id='NV')
        cls.test_user_b = User.register(username='test_user_b', password='test123', email='testuser_b@email.com', state_id='NV')
        db.session.add_all([cls.test_user, cls.test_user_b])
        db.session.commit()

    @classmethod
    def tearDownClass(cls):

        # remove test user
        db.session.delete(cls.test_user)
        db.session.delete(cls.test_user_b)
        db.session.commit()

        print("Teardown")

    # test if dashboard loads at root route when logged in
    def test_session_info_set(self):
        with app.test_client() as client:

            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id

            resp = client.get("/", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['user_id'], ViewsLoggedInTests.test_user.id)

    # test profile screen loads when logged in
    def test_profile_view(self):
        with app.test_client() as client:

            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id

            resp = client.get("/profile")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3 class="text-center text-sm-start mb-4">User Info: </h3>', html)

    # test if edit profile screen loads when logged in
    def test_edit_profile_view(self):
        with app.test_client() as client:

            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id

            resp = client.get("/profile/edit")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="text-center mt-3">Edit Profile</h1>', html)

    # test if delete account screen loads when logged in
    def test_delete_account_view(self):
        with app.test_client() as client:

            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id

            resp = client.get("/profile/delete")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3 class="text-center mb-5">Are you sure you want to delete your account?</h3>', html)

    # test logout success when logged in
    def test_delete_profile_view(self):
        with app.test_client() as client:

            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id

            resp = client.post("/logout", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Successfully logged out. See you later!', html)

    # test if login route redirects when user already logged in
    def test_login_view_li(self):
        with app.test_client() as client:

            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id

            resp = client.get("/login", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('You are already logged in! You must logout before signing into another account.', html)

    # test if signup route redirects when user already logged in
    def test_signup_view_li(self):
        with app.test_client() as client:

            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id

            resp = client.get("/signup", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('You are already logged in! You must logout before creating another account.', html)

    # test if logout works when user signed in
        def test_logout_li(self):
            with app.test_client() as client:

                with client.session_transaction() as change_session:
                    change_session['user_id'] = ViewsLoggedInTests.test_user.id

                resp = client.post("/logout", follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('Successfully logged out. See you later!', html)

    # test reject signup get request if already logged in
    def test_signup_while_logged_in_route(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id

            resp = client.get('/signup', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You are already logged in! You must logout before creating another account.', html)

    # test reject login get request if already logged in
    def test_login_route_while_logged_in(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id

            resp = client.get('/login', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You are already logged in! You must logout before signing into another account.', html)

    # test if duplicate username rejected on profile edit
    def test_edit_duplicate_username_route(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id
            d= {
                'username' : 'test_user_b',
                'email' : '123456testuser_a@email.com', 
                'state' : 'NV'
            }
            resp = client.post('/profile/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('That username is already taken! Please choose another.', html)
    
    # test if duplicate email rejected on profile edit
    def test_edit_duplicate_email_route(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id
            d= {
                'username' : 'test_user_10',
                'email' : 'testuser_b@email.com', 
                'state' : 'NV'
            }
            resp = client.post('/profile/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('There is already an account with that email. Please use another email.', html)

    # test if incorrect current password on password change
    def test_unauthenticated_password_change(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = ViewsLoggedInTests.test_user.id
            d= {
                'current_password' : 'test124',
                'new_password' : 'test567', 
            }
            resp = client.post('/password/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Current password incorrect. Please try again.', html)