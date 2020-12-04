from flask import Flask, request, render_template, redirect, session, flash, jsonify
import json
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from secrets import API_SECRET_KEY
from fileread import FileRead
import requests
import pprint
from models import db, connect_db, Bill, PolicyArea, User, BillFollows
from forms import BillForm, SignupForm, LoginForm
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

    if session.get('username', False):

        bill_ids = db.session.query(BillFollows.bill_id).filter(BillFollows.username == session['username']).all()

        print("***********************************")
        print("Bill Ids:", bill_ids)
        print(len(bill_ids))
        print("***********************************")

        bills = get_bills(bill_ids)

        if bills:


            return render_template('index.html', bills=bills)
        
        else:

            return render_template('index.html')

    else:

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

@app.route('/bill/<bill_id>/follow', methods=['POST'])
def follow_bill(bill_id):

    if session.get('username', False):

        bill = BillFollows.query.filter(BillFollows.bill_id == bill_id and BillFollows.username == session['username']).one_or_none()

        if bill:

            db.session.delete(bill)
            db.session.commit()
            return jsonify({'resp_code': 'unfoll_success'})

        
        else:
            new_bill_follow = BillFollows(bill_id = bill_id, username=session['username'])
            db.session.add(new_bill_follow)
            db.session.commit()
            return jsonify({'resp_code': 'foll_success'})

    else:
        # flash('You must be logged in to do that!')
        return jsonify({'resp_code': 'not_logged_in'})

@app.route('/legislators')
def view_legislators():


    return render_template('legislators.html')


# a page to give information on the chambers/ scronyms etc, mostly will be done in js dropping and revealing information
@app.route('/learn')
def view_learn_page():


    return render_template('learn.html')


@app.route('/home')
def show_homepage():

    if session.get('username', False):

        return render_template('home.html')

    else:
        flash('No user logged in')
        return redirect('/')

@app.route('/profile')
def show_profile():

    if session.get('username', False):


        user = User.query.filter(User.username==session['username']).first()

        return render_template('profile.html', user=user)

    else:
        flash('No user logged in')
        return redirect('/')



@app.route('/signup', methods=['GET','POST'])
def signup():

    form = SignupForm()

    if form.validate_on_submit():

        new_user = User.register(username = form.username.data, password = form.password.data, email = form.email.data)

        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username

        flash(f'New user: {new_user.username} added!')

        return redirect('/home')

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.authenticate(username = form.username.data, password = form.password.data)

        if user:

            session['username'] = user.username
            flash(f'User: {user.username} authenticated!')

            return redirect('/home')
        
        else:
            flash('User not authenticated!')
            return redirect('/login')

    else:
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():

    if session.get('username', False):
        session.pop('username')

        flash('Successfully logged out!')
        return redirect('/')
    
    else:
        flash('No user logged in')
        return redirect('/')

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


def get_bills(bill_ids):

    bills = []

    for bill_id in bill_ids:

        bill = Bill.query.filter(Bill.id == bill_id[0]).one_or_none()

        bills.append(bill)

    
    return bills