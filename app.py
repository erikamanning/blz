from flask import Flask, request, render_template, redirect, session, flash, jsonify
import json
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from secrets import API_SECRET_KEY
from fileread import FileRead
import requests
import pprint
from models import db, connect_db, Bill, PolicyArea
from forms import BillForm
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

@app.route('/bills/<bill_slug>')
def view_bill(bill_slug):

    bill = Bill.query.filter(Bill.bill_slug==bill_slug).one_or_none()

    if bill:

        return render_template("single_bill.html", bill=bill)

@app.route('/legislators')
def view_legislators():


    return render_template('legislators.html')
