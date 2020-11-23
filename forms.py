from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Optional, URL, NumberRange


class BillForm(FlaskForm):

    subject = SelectField('Choose a Bill Subject', validate_choice=False)


class LegislatorForm(FlaskForm):

    chamber = SelectField('Chamber', choices=[(1,"Senate"),(2,"House of Representatives")])