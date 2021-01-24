from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField, PasswordField, DateField
from wtforms.validators import InputRequired, Email, Optional, URL, NumberRange
from wtforms.fields.html5 import EmailField
CURRENT_SESSION = 116

class BillForm(FlaskForm):

    policy_area = SelectField('Policy Area', validate_choice=False,render_kw={'class':'form-control'})

class LegislatorForm(FlaskForm):

    position = SelectField('Position', validate_choice=False, render_kw={'class':'form-control'}, choices=[(0,'Any Position')])
    state = SelectField('State', validate_choice=False, render_kw={'class':'form-control'}, choices=[(0,'Any State')])
    party = SelectField('Party', validate_choice=False, render_kw={'class':'form-control'}, choices=[(0,'Any Party')])

class SignupForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired(message="Username cannot be blank")], render_kw={'class':'form-control'})
    password = PasswordField("Password", validators=[InputRequired(message="Password cannot be blank")], render_kw={'class':'form-control'})
    email = EmailField("Email", validators=[InputRequired(message="Email cannot be blank"),Email()], render_kw={'class':'form-control'})
    state = SelectField('State', render_kw={'class':'form-control'})

class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired(message="Username cannot be blank")], render_kw={'class':'form-control'})
    password = PasswordField("Password", validators=[InputRequired(message="Password cannot be blank")], render_kw={'class':'form-control'})

class EditProfile(FlaskForm):

    username = StringField("Username", validators=[InputRequired(message="Username cannot be blank")], render_kw={'class':'form-control'})
    email = EmailField("Email", validators=[InputRequired(message="Email cannot be blank"),Email()], render_kw={'class':'form-control'})
    state = SelectField('State', render_kw={'class':'form-control'})

class EditPassword(FlaskForm):

    current_password = PasswordField("Current Password", validators=[InputRequired(message="Current password is required.")], render_kw={'class':'form-control'})
    new_password = PasswordField("New Password", validators=[InputRequired(message="New password cannot be blank.")], render_kw={'class':'form-control'})

class DeleteUser(FlaskForm):

    delete_account = SubmitField(render_kw={'class':'btn btn-dark'})


class TestForm(FlaskForm):
    
    policy_area = SelectField('Subject', validate_choice=False,render_kw={'class':'form-control'})

