from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

class Add_user_form(Form):
    name = StringField('Name',[validators.Length(min = 1, max=50)])
    email_address = StringField('Email Address',[validators.Length(min = 1, max=50)])
    user_password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
