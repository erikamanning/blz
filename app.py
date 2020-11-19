from flask import Flask, request, render_template, redirect, session, flash, jsonify
import json
from flask_debugtoolbar import DebugToolbarExtension
# from classes import Bill
from flask_bcrypt import Bcrypt
from secrets import API_SECRET_KEY
from fileread import FileRead
import requests
import pprint
from models import db, connect_db, Subject, PolicyArea, State, Member, Chamber, Bill, Vote
from forms import BillForm
from utility import cure_query_str
from secrets import API_SECRET_KEY


headers = {'X-API-Key': API_SECRET_KEY}

pp = pprint.PrettyPrinter(indent=4)



app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lumine'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
debug = DebugToolbarExtension(app)


@app.route('/')
def show_home_page():

    return render_template('index.html')


@app.route('/get-data')
def get_data():

    req = requests.get('https://api.propublica.org/congress/v1/116/bills/s3955.json',headers=headers)

    resp_json = req.json()

    bill = Bill(resp_json["results"][0]["short_title"], resp_json["results"][0]["introduced_date"], resp_json["results"][0]["sponsor"], resp_json["results"][0]["summary"] )

    return jsonify(title=bill.title, date_created=bill.date_created, sponsor=bill.sponsor, summary=bill.summary)


@app.route('/bills', methods=["GET","POST"])
def view_bills():

    form = BillForm()

    subjects = db.session.query(Subject.id,Subject.name).all()

    form.subject.choices=subjects

    if form.validate_on_submit():

        subject_id = form.data["subject"]

        subject = Subject.query.get(subject_id)

        # cure strings of symbols that will break query string
        subject_name = cure_query_str(subject.name)

        req = requests.get(f'https://api.propublica.org/congress/v1/bills/subjects/{subject_name}.json',headers=headers)

        json_data = req.json()

        bills = json_data["results"]

        bills = store_bills(bills)

        return render_template('bills.html', subjects=subjects, form=form, bills=bills)

    else:

        return render_template('bills.html', subjects=subjects, form=form)

@app.route('/bills/<bill_id>')
def show_bill(bill_id):


    bill = Bill.query.filter(Bill.id==bill_id).one_or_none()

    # if not bill:


    sponsor = Member.query.get_or_404(bill.sponsor_id)

    print("***********************************")
    print("Bill : ", bill)
    print("***********************************")

    return render_template('single_bill.html', bill=bill, sponsor=sponsor)


@app.route('/legislators')
def view_legislators():

    # 
    members = Member.query.all()


    return render_template('legislators.html', members = members)

@app.route('/legislators/<legislator_id>')
def show_legislator(legislator_id):

    legislator = Member.query.get_or_404(legislator_id)

    req = requests.get(f'https://api.propublica.org/congress/v1/members/{legislator_id}/votes.json', headers=headers)

    json = req.json()

    vote_data = json["results"][0]["votes"]

    votes = get_votes(vote_data)

    return render_template('single_legislator.html', legislator=legislator, votes=votes)

def get_bill_names(bills):

    bill_names = []
    count = 0

    for bill in bills:

        count+=1
        # print(count)
        bill_names.append(bill["short_title"])

    return bill_names


# gets 20 most recently introduced bills from a chamber specified
# may need to do a join later to get recent bills from both the house and the senate and display them both
def get_recent_bills():

    data_req = requests.get('https://api.propublica.org/congress/v1/116/house/bills/introduced.json',headers=headers)

    resp_json = data_req.json()

    bills = resp_json["results"][0]["bills"]

    # may need to change this later, don't want to be extracting from JSON through the program. Get what we need, store in Db and get out

    return bills

def get_bills_by_subject(subject):

    req = requests.get('https://api.propublica.org/congress/v1/116/house/bills/introduced.json', headers=headers)

    return 0


def store_bills(bills):

    stored_bills = []

    for bill in bills:

        bill_id =  bill["bill_id"]
        bill_stored= check_bill_stored(bill_id)

        if not bill_stored:

            title = bill["short_title"]
            sponsor_id = bill["sponsor_id"]

            new_bill = Bill(id=bill_id, title=title, sponsor_id=sponsor_id )
            stored_bills.append(new_bill)
            db.session.add(new_bill)
            db.session.commit()

        else:

            stored_bills.append(bill_stored)
    
    return stored_bills

def check_bill_stored(bill_id):

    status = Bill.query.filter(Bill.id==bill_id).one_or_none()

    return status

def get_votes(vote_data):


    votes = []

    for vote in vote_data:

        new_vote = {
            "bill_title" : vote["bill"]["title"],
            "member_id" : vote["member_id"], 
            "bill_id" : vote["bill"]["bill_id"], 
            "response" : vote["position"],
            "bill_uri" : vote["bill"]["bill_uri"]
        }
        votes.append(new_vote)



    return votes

def add_bill(bill_uri):

    return 0

