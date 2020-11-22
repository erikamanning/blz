from app import db, headers
from models import Subject
import requests

Subject.__table__.drop(db.get_engine())
Subject.__table__.create(db.get_engine())

def get_subject_json_data(req_str):

    req = requests.get('https://api.propublica.org/congress/v1/bills/subjects/search.json?offset=20', headers=headers)

    req_json = req.json()

    subject_json = req_json["results"][0]["subjects"]

    return subject_json

def extract_subject_names(subject_json):

    subject_names = []

    for block in subject_json:

        subject_names.append(block["name"])

    return subject_names

def save_subjects(subject_names):

    subjects = []

    for subject_name in subject_names:

        new_subject = Subject(name=subject_name)
        subjects.append(new_subject)

    db.session.add_all(subjects)
    db.session.commit()

def get_all_subjects():

    # all_subject_names = []

    # priming loop
    amount_received = 20

    num_subjects = 20
    i=0

    print("Calls: ")
    while amount_received >= 20:

        offset = i*num_subjects

        req = requests.get(f'https://api.propublica.org/congress/v1/bills/subjects/search.json?offset={offset}', headers=headers)

        req_json = req.json()

        subject_json = req_json["results"][0]["subjects"]

        subject_names = extract_subject_names(subject_json)

        save_subjects(subject_names)

        # all_subject_names.append([subject_name for subject_name in subject_names])

        amount_received = len(subject_names)

        print(i)

        i+=1




# main work
# subject_json_data = get_subject_json_data()
all_subject_names = get_all_subjects()
