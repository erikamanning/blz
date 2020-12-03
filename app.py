from flask import Flask, request, render_template, redirect, session, flash, jsonify
import json
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from secrets import API_SECRET_KEY
from fileread import FileRead
import requests
import pprint
from models import db, connect_db, Bill, PolicyArea, User
from forms import BillForm, SignupForm
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


@app.route('/bills', methods=["GET", "POST"])
def view_bills():

    policy_areas = db.session.query(PolicyArea.id, PolicyArea.name).all()

    form = BillForm()
    form.subject.choices = policy_areas

    if form.validate_on_submit():

        policy_area_id = form.subject.data
        policy_area = PolicyArea.query.get(policy_area_id)

        bills = Bill.query.filter(Bill.primary_subject==policy_area.name).order_by(Bill.introduced_date.asc()).limit(20).all()

        print("***********************************")
        print("Num Bills:")
        print(len(bills))
        print("***********************************")


        return render_template('bills.html', form=form, bills=bills)
    
    else:

        return render_template('bills.html', form=form)

@app.route('/bills/<bill_id>')
def view_bill(bill_id):

    bill = Bill.query.get_or_404(bill_id)

    # bill = Bill.query.filter(Bill.bill_slug==bill_slug).one_or_none()

    if bill:

        summary = prune_summary(bill.summary)
    
        return render_template("single_bill.html", bill=bill, summary=summary)

@app.route('/legislators')
def view_legislators():


    return render_template('legislators.html')


# a page to give information on the chambers/ scronyms etc, mostly will be done in js dropping and revealing information
@app.route('/learn')
def view_learn_page():


    return render_template('learn.html')


@app.route('/signup', methods=['GET','POST'])
def signup():

    form = SignupForm()

    if form.validate_on_submit():

        return redirect('/')

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():

    return 0









#temporary fix for api keeping title awkwardly in summary, will update full database eventually
def prune_summary(summary):

    if 'This bill' in summary:

        find_index = summary.find('This bill')
        
        lst = summary[find_index::]

        print('Pruned summary: ', lst)

        new_summary = str(lst)

        return new_summary
    
    else:

        return summary


app.jinja_env.globals.update(prune_summary=prune_summary)


