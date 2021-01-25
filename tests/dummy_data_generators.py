from app import app, db, CURRENT_CONGRESS_SESSION
from models import Bill, Legislator, PolicyArea, Party, State
from get_app_data.get_bill_data_utility_functions import handle_policy_area, add_sponsored_bill


def add_dummy_party(party_code, party_name):

    dummy_party = Party(code =party_code, name= party_name)
    db.session.add(dummy_party)
    db.session.commit()

def add_dummy_state(state_acronym, state_name):

    dummy_state = State( acronym=state_acronym, name= state_name)
    db.session.add(dummy_state)
    db.session.commit()

def add_dummy_legislator( legislator_id, last_name, state, position, party):
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

def remove_dummy_legislators():

    for dummy_legislator in Legislator.query.filter(Legislator.id.contains('dummy')).all():

        db.session.delete(dummy_legislator)
        db.session.commit()

def remove_dummy_parties():

    for dummy_party in Party.query.filter(Party.code.contains('dummy')).all():

        db.session.delete(dummy_party)
        db.session.commit()

def remove_dummy_states():

    for dummy_state in State.query.filter(State.acronym.contains('dummy')).all():

        db.session.delete(dummy_state)
        db.session.commit()

def add_dummy_bill( bill_id, sponsor_id, policy_area,introduced_date, latest_major_action_date ):

    new_bill = Bill(
            id = f'dummy_bill_{bill_id}',
            bill_slug = 'dummy_slug',
            congress = CURRENT_CONGRESS_SESSION,        
            bill = 'dummy_bill',            
            bill_type = 'dummy_bill_type',
            number = 'dummy_number',
            title = 'dummy_title',
            short_title = 'dummy_short_title',
            sponsor_id = sponsor_id,
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

def remove_dummy_bills():

    dummy_bills = Bill.query.filter(Bill.id.contains('dummy_bill_')).all()

    for bill in dummy_bills:

        db.session.delete(bill)
        db.session.commit()

def remove_dummy_policy_areas():

    dummy_policy_areas = PolicyArea.query.filter(PolicyArea.name.contains('dummy')).all()

    for policy_area in dummy_policy_areas:

        db.session.delete(policy_area)
        db.session.commit()