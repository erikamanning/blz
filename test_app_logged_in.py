from unittest import TestCase
from app import app, db
from flask import session
from models import User

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class ViewsLoggedInTests(TestCase):

    @classmethod
    def setUpClass(cls):

        # add test user
        cls.test_user = User.register(username='test_user3', password='test123', email='test3@email.com', state_id='NV')
        db.session.add(cls.test_user)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):

        # remove test user
        db.session.delete(cls.test_user)
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

    # test if delete profile screen loads when logged in
    def test_delete_profile_view(self):
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