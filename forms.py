from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField, PasswordField, DateField
from wtforms.validators import InputRequired, Email, Optional, URL, NumberRange
from wtforms.fields.html5 import EmailField


class BillForm(FlaskForm):

    policy_area = SelectField('Subject', validate_choice=False,render_kw={'class':'form-control'}, default=0)
    session = SelectField('Session', validate_choice=False, default = '116',render_kw={'class':'form-control'})

class LegislatorForm(FlaskForm):

    chamber = SelectField('Chamber', choices=[(1,"Senate"),(2,"House of Representatives")])

class SignupForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired(message="Username cannot be blank")], render_kw={'class':'form-control'})
    password = PasswordField("Password", validators=[InputRequired(message="Password cannot be blank")], render_kw={'class':'form-control'})
    email = EmailField("Email", validators=[InputRequired(message="Email cannot be blank"),Email()], render_kw={'class':'form-control'})


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired(message="Username cannot be blank")], render_kw={'class':'form-control'})
    password = PasswordField("Password", validators=[InputRequired(message="Password cannot be blank")], render_kw={'class':'form-control'})