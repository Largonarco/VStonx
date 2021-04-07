from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(),])
    password = PasswordField('Password', validators=[DataRequired(), ])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password') ])
    submit = SubmitField('Sign Up')

class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), ])
    password = PasswordField('Password', validators=[DataRequired(),  ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')