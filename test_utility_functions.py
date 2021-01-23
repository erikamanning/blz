from unittest import TestCase
from app import app, db, convert_date, check_user_info_messages, post_edit_submit_message
from models import User, Bill, BillFollows, PolicyArea,SponsoredBill
from get_bill_data_utility_functions import get_slugs, prune_summary,handle_policy_area, add_sponsored_bill

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class TestUtilityFunctions(TestCase):


    def test_date_conversion(self):

        good_date = '2021-01-14'

        converted_date = convert_date(good_date)
        self.assertEqual(converted_date, 'January 14, 2021')

    def test_check_user_info_messages(self):

        username_1 = False
        email_1 = False

        username_2 = True
        email_2 = True


        messages_1 = check_user_info_messages(username_1,email_1)
        messages_2 = check_user_info_messages(username_2,email_2)
        messages_3 = check_user_info_messages(username_2,email_1)
        messages_4 = check_user_info_messages(username_1,email_2)


        # both username and email unique
        self.assertEqual(messages_2, [])
        self.assertFalse(messages_2)

        # both username and email duplicates
        self.assertEqual(len(messages_1), 2)
        self.assertIn('That username is already taken! Please choose another.',messages_1)
        self.assertIn('There is already an account with that email. Please use another email.',messages_1)

        # only email is duplicate
        self.assertEqual(len(messages_3), 1)
        self.assertNotIn('That username is already taken! Please choose another.',messages_3)
        self.assertIn('There is already an account with that email. Please use another email.',messages_3)

        # only username is duplicate
        self.assertEqual(len(messages_4), 1)
        self.assertIn('That username is already taken! Please choose another.',messages_4)
        self.assertNotIn('There is already an account with that email. Please use another email.',messages_4)


    def test_post_edit_submit_message(self):

        changes_made1 = False
        changes_made2 = True

        messages1 = post_edit_submit_message(changes_made1)
        messages2 = post_edit_submit_message(changes_made2)

        # only username is duplicate
        self.assertEqual('No changes were made.',messages1)

        # only username is duplicate
        self.assertEqual('Your information has been updated!',messages2)

    def test_get_slugs(self): 

        bill_data = [
            {
                'bill_slug':'a',
            },

            {
                'bill_slug':'b',
            },
            
            {
                'bill_slug':'c',
            }
        ]

        slugs = get_slugs(bill_data)

        self.assertIn('a', slugs)
        self.assertIn('b', slugs)
        self.assertIn('c', slugs)
        self.assertEqual(len(slugs), 3)
        
    def test_prune_summary(self): 

        bill1 = 'This bill Creates a commission build a robot duck. A robot duck will be built and 10 billion will be allocated.'
        bill2 = 'A commission will be created to judge the spelling skills of golden retrievers.' 

        summary1 = prune_summary(bill1)
        summary2 = prune_summary(bill2)

        # bill pruned of duplicate data from API
        self.assertEqual(summary1, 'Creates a commission build a robot duck. A robot duck will be built and 10 billion will be allocated.')
        
        # no pruning necessary
        self.assertEqual(summary2, bill2)

        
    def test_handle_policy_area(self): 

        # get current num policy areas
        num_policy_areas = len(PolicyArea.query.all())

        # add new policy area
        test_policy_area_name = 'test_policy_area_1'
        handle_policy_area(test_policy_area_name)

        # test add new policy area name
        self.assertTrue(PolicyArea.query.filter(PolicyArea.name == test_policy_area_name).one_or_none())
        self.assertEqual(num_policy_areas+1, len(PolicyArea.query.all()))
        num_policy_areas +=1

        handle_policy_area(test_policy_area_name)

        # test add duplicate
        self.assertNotEqual(num_policy_areas+1, len(PolicyArea.query.all()))

        # cleanup
        test_policy_area =PolicyArea.query.filter(PolicyArea.name == test_policy_area_name).one_or_none()
        db.session.delete(test_policy_area)
        db.session.commit()
        
