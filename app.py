from flask import Flask, request, render_template, redirect, session, flash, jsonify, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Bill, PolicyArea, User, BillFollows, Legislator, Party, State, Position
from forms import BillForm, SignupForm, LoginForm, LegislatorForm, EditProfile, DeleteUser, EditPassword, TestForm
from sqlalchemy.exc import IntegrityError
from flask.cli import with_appcontext
from initialize_app import initialize_database
from update_app import update_db
from sqlalchemy import and_
import os
import requests
import click

try:
    from secrets import API_SECRET_KEY
except:
    API_SECRET_KEY = 'NOT A KEY'

CURRENT_CONGRESS_SESSION = 117
CURRENT_USER_ID = 'user_id'
LEGISLATOR_DEFAULT_IMAGE_PATH = '/static/congressmen_default.png'
ROWS_PER_PAGE = 10
headers = {'X-API-Key': os.environ.get('SECRET-API-KEY', API_SECRET_KEY)}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','2@!4q18&5l!D32d%^!#4')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///blz')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
debug = DebugToolbarExtension(app)

@click.command(name='init_app')
@with_appcontext
def init_app():

    initialize_database(db)

app.cli.add_command(init_app)

@click.command(name='update_app')
@with_appcontext
def update_app():

    update_db(CURRENT_CONGRESS_SESSION)

app.cli.add_command(update_app)

@app.before_request
def add_user_to_g():

    g.legislator_default_image_path = LEGISLATOR_DEFAULT_IMAGE_PATH

    if CURRENT_USER_ID in session:

        g.user = User.query.get(session[CURRENT_USER_ID])

    else:

        g.user = None

def do_login(user):

    session[CURRENT_USER_ID] = user.id

def do_logout():

    if CURRENT_USER_ID in session:

        del session[CURRENT_USER_ID]

@app.route('/')
def show_home_page():

    if session.get(CURRENT_USER_ID, False):

        return redirect('/dashboard')

    else:

        return render_template('index.html')

@app.route('/bills', methods=['GET'])
def view_bills():

    form = configure_bill_search_form(BillForm(request.args))

    page = request.args.get('page', 1, type=int)
    results = process_bill_search_request(request.args)
    bills = Bill.query.filter(and_(*results['filter_args'])).order_by(Bill.introduced_date.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)

    messages = show_mesages(results['messages'])
    return render_template('bills/bills.html', end_date = results['end_date'], start_date=results['start_date'], form=form, bills=bills)

@app.route('/bill/<bill_id>')
def view_bill(bill_id):

    bill = Bill.query.get_or_404(bill_id)

    if bill:
    
        return render_template("bills/bill_single.html", bill=bill)

@app.route('/bill/<bill_id>/follow', methods=['POST'])
def follow_bill(bill_id):

    if session.get(CURRENT_USER_ID, False):

        bill_follow = BillFollows.query.filter(BillFollows.bill_id == bill_id and BillFollows.user_id == session[CURRENT_USER_ID]).one_or_none()

        if bill_follow:

            db.session.delete(bill_follow)
            db.session.commit()
            return jsonify({'resp_code': 'unfoll_success'})

        else:
            new_bill_follow = BillFollows(bill_id = bill_id, user_id=session[CURRENT_USER_ID])
            db.session.add(new_bill_follow)
            db.session.commit()
            return jsonify({'resp_code': 'foll_success'})

    else:
        return jsonify({'resp_code': 'not_logged_in'})

@app.route('/legislators')
def view_legislators():

    form = configure_legislator_form(LegislatorForm(request.args))

    page = request.args.get('page', 1, type=int)
    filter_args = get_legislator_filter_args(request.args)

    legislators = Legislator.query.filter(and_(*filter_args)).order_by(Legislator.last_name).paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('legislators/legislators.html', legislators = legislators, form=form)

@app.route('/legislator/<legislator_id>')
def view_legislator(legislator_id):

    legislator = Legislator.query.filter(Legislator.id==legislator_id).first()
    sponsored_bills = legislator.sponsored_bills

    return render_template('legislators/legislator_single.html', legislator = legislator, sponsored_bills=sponsored_bills)

@app.route('/dashboard')
def show_homepage():

    if session.get(CURRENT_USER_ID, False):

        user = User.query.filter(User.id==int(session[CURRENT_USER_ID])).one_or_none()

        if user and user.state_id != 'NONE':

            senators = Legislator.query.filter(Legislator.state_id==user.state_id, Legislator.position_code=='Sen.', Legislator.in_office==True).order_by(Legislator.last_name).all()
            representatives = Legislator.query.filter(Legislator.state_id==user.state_id, Legislator.position_code=='Rep.', Legislator.in_office==True).order_by(Legislator.last_name).all()
            legislators = {'s':senators, 'r':representatives}

            return render_template('user/dashboard.html', user=user, bills=user.followed_bills, legislators=legislators)

        return render_template('user/dashboard.html', user=user, bills=user.followed_bills)

    else:
        flash('You must be logged in to do that!')
        return redirect('/')

@app.route('/profile')
def show_profile():

    if session.get(CURRENT_USER_ID, False):

        user = User.query.filter(User.id==int(session[CURRENT_USER_ID])).first()
        return render_template('user/profile.html', user=user)

    else:

        flash('You must be logged in to do that!')
        return redirect('/')

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():

    if session.get(CURRENT_USER_ID,False):

        user = User.query.filter(User.id==int(session[CURRENT_USER_ID])).one_or_none()

        user_form_obj = {

            'username': user.username,
            'email': user.email,
            'state': user.state_id
        }

        # create forms/ fill form data
        edit_password_form = EditPassword()
        edit_profile_form = EditProfile(data=user_form_obj)

        states = db.session.query(State.acronym, State.name).all()
        edit_profile_form.state.choices = states

        # handle form submit
        if edit_profile_form.validate_on_submit():

            # check if changes to profile conflict with other users' data
            data_check = user.edit_profile_check(username = edit_profile_form.username.data, email = edit_profile_form.email.data)
            messages = check_user_info_messages(data_check['username_check'], data_check['email_check'])

            # let user know about conflicts and refresh
            if messages:

                for message in messages:
                    flash(message)
                
                return redirect('/profile/edit')

            # otherwise make edits and refresh
            else:

                changes_made = user.edit_profile(edit_profile_form.username.data,edit_profile_form.email.data,edit_profile_form.state.data)
                message = post_edit_submit_message(changes_made)
                flash(message)
                return render_template('user/edit_profile.html', user=user, edit_profile_form=edit_profile_form, edit_password_form=edit_password_form)

        else:

            return render_template('user/edit_profile.html', user=user, edit_profile_form=edit_profile_form, edit_password_form=edit_password_form)

    else:

        flash('You must be logged in to do that!')
        return redirect('/')

@app.route('/password/edit', methods=['POST'])
def edit_password():
    
    form = EditPassword()

    if session.get(CURRENT_USER_ID,False):

        user = User.query.filter(User.id==int(session[CURRENT_USER_ID])).one_or_none()

        if form.validate_on_submit():

            authenticated = User.authenticate(username=g.user.username, password=form.current_password.data)

            if authenticated:

                user.change_password(form.new_password.data)   
                db.session.add(user)
                db.session.commit()

                flash('Password successfully changed!')
                return redirect('/profile/edit')      

            else:

                flash('Current password incorrect. Please try again.')
                return redirect('/profile/edit')
        else:

            return redirect('/profile/edit')

    else:

        flash('You must be logged in to do that!')
        return reroute('/login')  

@app.route('/profile/delete', methods=['GET','POST'])
def delete_account():

    if session.get(CURRENT_USER_ID, False):

        form = DeleteUser()

        if form.validate_on_submit():

            user_id = session[CURRENT_USER_ID]
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()

            flash('Your account has been deleted.')
            do_logout()
            return redirect('/')

        else:

            return render_template('user/delete_form.html', form=form)

    else:

        flash('You must be logged in to do that!')
        return redirect('/')

@app.route('/signup', methods=['GET','POST'])
def signup():

    if session.get(CURRENT_USER_ID,False):

        flash("You are already logged in! You must logout before creating another account.")
        return redirect('/')
        
    else:

        form = SignupForm()
        states = db.session.query(State.acronym, State.name).all()    
        form.state.choices = states

        if form.validate_on_submit():

            submitted_username = form.username.data
            submitted_email = form.email.data
            messages = check_user_info_messages( User.check_for_duplicate_username(submitted_username), User.check_for_duplicate_email(submitted_email) )

            if messages:

                for message in messages:
                    flash(message)
                
                return redirect('/signup')

            else:

                new_user = User.register(username = form.username.data, password = form.password.data, email = form.email.data, state_id = form.state.data)
                db.session.add(new_user)
                db.session.commit()

                session[CURRENT_USER_ID] = new_user.id

                flash(f'Welcome {new_user.username}!')

                return redirect('/dashboard')

        else:
            
            return render_template('user/signup.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():

    if session.get(CURRENT_USER_ID,False):

        flash("You are already logged in! You must logout before signing into another account.")
        return redirect('/')

    else:
        form = LoginForm()

        if form.validate_on_submit():

            user = User.authenticate(username = form.username.data, password = form.password.data)

            if user:

                do_login(user)
                flash(f'Welcome back {user.username}!')
                return redirect('/dashboard')
            
            else:

                flash('Login information not correct! Please try again.',"alert alert-light text-center")
                return redirect('/login')

        else:

            return render_template('user/login.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():

    if session.get(CURRENT_USER_ID, False):

        do_logout()

        flash('Successfully logged out. See you later!')
        return redirect('/')
    
    else:

        flash('No user currently logged in!')
        return redirect('/')

@app.route('/user/<int:user_id>/followed-bills')
def get_followed_bills(user_id):

    if session.get(CURRENT_USER_ID,False):

        followed_bill_ids = db.session.query(BillFollows.bill_id).filter(BillFollows.user_id == user_id )
        bill_ids = [el[0] for el in followed_bill_ids ]

        return jsonify(bill_ids)

    else:

        flash('Access denied!')
        return redirect('/')

# function to convert date to different format
def convert_date(date_str):

    months = {

        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    date_data = date_str.split('-')
    month = months[int(date_data[1])]
    new_date_str = f'{month} {date_data[2]}, {date_data[0]}'

    return new_date_str

app.jinja_env.globals.update(convert_date=convert_date)

def check_user_info_messages(username_good,email_good):

    messages = []

    if not username_good:

        messages.append('That username is already taken! Please choose another.')

    if not email_good:

        messages.append('There is already an account with that email. Please use another email.')        

    return messages

def post_edit_submit_message(changes_made):

    if changes_made:

        message = 'Your information has been updated!'

    else:

        message = 'No changes were made.'

    return message

def show_mesages(messages):

    for message in messages:

        flash(message)

def process_bill_search_request(request_args):

    results = {'filter_args':[],'end_date': '', 'start_date': '', 'messages':[] }

    if request_args.get('policy_area',False):

        try: 
            int(request_args['policy_area'])

        except ValueError:
            results['messages'].append('Sorry! That is not a valid policy area!')

        else:
            policy_area_id = request_args['policy_area']
            policy_area = PolicyArea.query.get_or_404(policy_area_id)
            results['filter_args'].append(Bill.primary_subject == policy_area.name )

    #start date/ end date
    if request_args.get('start_date',False):

        results['start_date'] = request_args['start_date']
        results['filter_args'].append(Bill.introduced_date >= results['start_date'])

    if request_args.get('end_date',False):

        results['end_date'] = request_args['end_date']
        results['filter_args'].append(Bill.introduced_date <= results['end_date'])

    return results

def configure_bill_search_form(form):

    any_subject = ('','Any Subject') 
    form.policy_area.choices = db.session.query(PolicyArea.id,PolicyArea.name).order_by(PolicyArea.name).all()
    form.policy_area.choices.insert(0,any_subject)

    return form

def get_legislator_filter_args(request_args):

    filter_args=[]

    if request_args.get('state',False) and request_args.get('state') != '0':

        state_code = request_args['state']
        filter_args.append(Legislator.state_id == state_code)

    if request_args.get('party',False) and request_args.get('party') != '0':

        party_code = request_args['party']
        filter_args.append(Legislator.party_id == party_code)

    if request_args.get('position',False) and request_args.get('position') != '0':

        position_code = request_args['position']
        filter_args.append(Legislator.position_code == position_code)

    return filter_args

def configure_legislator_form(form):

    parties = db.session.query(Party.code,Party.name).all()
    states = db.session.query(State.acronym,State.name).all()
    positions = db.session.query(Position.code,Position.name).all()

    for position in positions:

        form.position.choices.append(position)

    for party in parties:

        form.party.choices.append(party)

    for state in states:

        form.state.choices.append(state)  

    return form