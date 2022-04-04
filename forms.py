from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired(), ])
    submit = SubmitField('')

class DropdownForm(FlaskForm):
    index = SelectField('Indices', choices=[('NIFTY50', 'NIFTY 50'), ('NIFTY_M50', 'NIFTY MIDCAP 50'), ('NIFTY_S50', 'NIFTY SMALLCAP 50')], validators=[DataRequired()])
    submit = SubmitField('')
