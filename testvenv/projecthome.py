from flask import Flask, render_template, request, flash, redirect, url_for, session, logging, jsonify, make_response, current_app  
import json
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
import pymongo
from Forms import Add_user_form
from functools import update_wrapper
from flask_cors import CORS, cross_origin
from datetime import timedelta 

app = Flask(__name__)
CORS(app)

firebase = firebase.FirebaseApplication('https://myapplication-8f68b.firebaseio.com/', None)

# initialize firebase_admin
##cred = credentials.Certificate('D:\Rakesh\Data\PROJECT\myapplication-8f68b-4fe5e0c2c8a0.json')
##firebase_admin.initialize_app(cred)
# initialize mongodb
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["localdb"]

##db = firestore.client()

@app.route('/')
def index():
    result = firebase.get('/users', None)
    return render_template('home.html')

@app.route('/get_users', methods=['GET'])
def get_all_users():
    userdata = ''
    result = firebase.get('/users', None)
    for x, y in result.items():
        userdata = userdata + json.dumps(y)
    return jsonify(userdata)

@app.route('/get_events', methods = ['GET'])
def get_all_events():
    eventdata = ''
    result = firebase.get('/events', None)
    for x, y in result.items():
        eventdata = eventdata + json.dumps(y)
    return jsonify(eventdata)

@app.route('/get_locations', methods=['GET'])
def get_all_locations():
    locationdata = ''
    result = firebase.get('/locations', None)
    for x, y in result.items():
        locationdata = locationdata + json.dumps(y)
    return jsonify(locationdata)

@app.route('/get_organisers', methods =['GET'])
def get_all_organisers():
    organisersdata=''
    result = firebase.get('/event_users', None)
    for x, y in result.items():
        organisersdata = organisersdata + json.dumps(y)
        return jsonify(organisersdata)

@app.route('/add_event', methods =['POST','PUT'])
def add_event():
    return render_template('home.html')
    

@app.route('/add_user', methods =['POST','PUT','OPTIONS'])
##@crossdomain(origin='*')
def add_user():
    if request.method == 'POST':
        data = request.data
        print(data)
        dataDict = json.loads(data)
        ##print(dataDict)
        ##u_id = firebase.push()
        result = firebase.post("/users", dataDict)
        print(result)
        # response = make_response(result) 
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5000')
        # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        # response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return result

    return redirect(url_for('index'))

@app.route('/add_location', methods =['POST','PUT'])
def add_location():
    return render_template('home.html')

@app.route('/add_committee_members', methods =['POST','PUT'])
def add_committee_members():
    return render_template('home.html')

@app.route('/add_user_page')
def add_user_page():
	form = Add_user_form(request.form)
	return render_template('registration.html', form = form)

def crossdomain(origin):  
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator 

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
