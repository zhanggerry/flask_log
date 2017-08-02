#-*- coding: utf-8 -*-
#!E:\python\python.exe


from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Required


class LoginForm(Form):
    username = StringField('please enter your username?', validators=[Required()])
    password = PasswordField('please enter your password?', validators=[Required()])
    remeber  = BooleanField('remeber me?')
    submit = SubmitField('Submit')

