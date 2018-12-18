from flask import Flask, render_template, request, flash, redirect, url_for, session, logging, jsonify
import json
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pymongo
from Forms import Add_user_form

app = Flask(__name__)

firebase = firebase.FirebaseApplication('https://myapplication-8f68b.firebaseio.com/', None)

# initialize firebase_admin
cred = credentials.Certificate('D:\Rakesh\Data\PROJECT\myapplication-8f68b-4fe5e0c2c8a0.json')
firebase_admin.initialize_app(cred)
# initialize mongodb
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["localdb"]

db = firestore.client()

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
    

@app.route('/add_user', methods =['POST','PUT'])
def add_user():
    form = Add_user_form(request.form)
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        print(dataDict)

        return (jsonify(dataDict))

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

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
