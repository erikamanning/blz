from models import Legislator, Party, State
from app import headers,db, CURRENT_SESSION


def add_dummy_party(party_code, party_name):

    dummy_party = Party(code =party_code, name= party_name)
    db.session.add(dummy_party)
    db.session.commit()

def add_dummy_state(state_acronym, state_name):

    dummy_state = State( acronym=state_acronym, name= state_name)
    db.session.add(dummy_state)
    db.session.commit()

def add_dummy_legislator(legislator_id, last_name, state, position, party):
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