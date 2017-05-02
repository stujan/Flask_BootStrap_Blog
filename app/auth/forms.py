__author__ = 'sanjay'

from flask_wtf import  Form
from wtforms import  StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import  Required,length

class LoginForm(Form):
    username = StringField('username',validators=[Required()])
    password = PasswordField('password',validators=[Required()])

    remember_me = BooleanField('Keep me')
    submit = SubmitField("Log In")


