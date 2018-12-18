from flask import Flask, render_template, request, flash, redirect, url_for, session, logging, jsonify
from firebase import firebase
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import json
from functools import wraps
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)
app.config ['MONGO_DBNAME'] = 'localhost'
app.config ['MONGO_URI'] = 'mongodb://rakeshvasaldbadmin:rakeshvasal02@ds259912.mlab.com:59912/oddesseydb'

mongo = PyMongo(app)

##firebase = firebase.FirebaseApplication('https://androidone-43cbb.firebaseio.com/', None)
firebase = firebase.FirebaseApplication('https://myapplication-8f68b.firebaseio.com/', None)

myclient = pymongo.MongoClient("mongodb://rakeshvasaldbadmin:rakeshvasal02@ds259912.mlab.com:59912/oddesseydb")

mydb = myclient["oddesseydb"]

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login')
def login_controller():
	if request.method == 'POST':
		str_username = request.form['username']
		str_password = request.form['password']

	return render_template('login.html', error = error)


@app.route('/login_page')
def login_page():
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    userlist = []
    result = firebase.get('/users', None)
    for x, y in result.items():
        userdata = json.dumps(y)
        lastindex = userdata.rindex('}')
        userdata = userdata[:lastindex]
        userdata = userdata + " ,\"id\" : \"" + x + "\"}"
        d_list = json.loads(userdata)
        ##userlist.append(d_list)

    return render_template('displayallusers.html', users=userlist)




## Add User Api Call
@app.route('/add_user', methods=['GET','POST'])
def add_user():
	form = Add_user_form(request.form)
	if request.method == 'POST' and form.validate():

		user = {}
		name = form.name.data
		contact_no = form.contact_no.data
		user_name = form.user_name.data
		course_year = form.course_year.data
		photourl = form.photourl.data
		role = form.role.data
		branch = form.branch.data
		email = form.email_address.data
		user_password = form.user_password.data
		user['name'] = name
		user['user_email'] = email
		user['user_name'] = user_name
		user['user_id'] = 1
		user['contact_no'] = contact_no
		user['password'] = user_password
		user['course_year'] = ""
		user['photourl'] = ""
		user['role'] = ""
		user['branch'] = ""
		user['google_id'] = ""
		json_data = json.dumps(user)
		json_str = json.loads(json_data)
		##u_id = firebase.push()
		result = firebase.post("/users", json_str)

		##print(result)

	return redirect(url_for('dashboard'))

## redirects the user to the html page for adding a user
@app.route('/add_user_page')
def add_user_page():
	form = Add_user_form(request.form)
	return render_template('registration.html', form = form)

## Add Delete Api Call
@app.route('/delete_user/<string:id>', methods=['POST'])
def delete_user(id):
    flash('Article Deleted', 'success')
    return redirect(url_for('dashboard'))

## Form for Creating a user using wtforms
class Add_user_form(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email_address = StringField('Email Address', [validators.Length(min=1, max=50)])
    user_name = StringField('UserName', [validators.Length(min=1, max=50)])
    contact_no = StringField('Contact Number', [validators.Length(min=1, max=50)])
    course_year = StringField('Course Year', [validators.Length(min=1, max=50)])
    photourl = StringField('Photo URL', [validators.Length(min=1, max=50)])
    role = StringField('Role', [validators.Length(min=1, max=50)])
    branch = StringField('Branch', [validators.Length(min=1, max=50)])
    user_password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')



if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
