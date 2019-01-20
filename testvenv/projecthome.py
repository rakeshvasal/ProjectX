from flask import Flask, render_template, request, flash, redirect, url_for, session, logging, jsonify, make_response, current_app
import json
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
import pymongo
from Forms import Add_user_form


app = Flask(__name__)

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

## GET REQUESTS
@app.route('/api/v1/get_users', methods=['GET'])
def get_all_users():
    userdata = ''
    result = firebase.get('/users', None)
    for x, y in result.items():
        userdata = userdata + json.dumps(y)
    return jsonify(userdata)

@app.route('/api/v1/get_events', methods = ['GET'])
def get_all_events():
    eventdata = ''
    result = firebase.get('/events', None)
    for x, y in result.items():
        eventdata = eventdata + json.dumps(y)
    return jsonify(eventdata)

@app.route('/api/v1/get_locations', methods=['GET'])
def get_all_locations():
    locationdata = ''
    result = firebase.get('/locations', None)
    for x, y in result.items():
        locationdata = locationdata + json.dumps(y)
    return jsonify(locationdata)

@app.route('/api/v1/get_organisers', methods =['GET'])
def get_all_organisers():
    organisersdata=''
    result = firebase.get('/event_users', None)
    for x, y in result.items():
        organisersdata = organisersdata + json.dumps(y)
        return jsonify(organisersdata)

## POST REQUESTS
@app.route('/api/v1/add_event', methods =['POST'])
def add_event():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = firebase.post("/events", dataDict)
        return jsonify(result)

    return redirect(url_for('index'))

@app.route('/api/v1/add_user', methods =['POST'])
def add_user():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = firebase.post("/users", dataDict)
        return jsonify(result)

    return redirect(url_for('index'))

@app.route('/api/v1/add_location', methods =['POST'])
def add_location():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = firebase.post("/locations", dataDict)
        return jsonify(result)
    return render_template('home.html')

@app.route('/api/v1/add_organisers', methods =['POST'])
def add_committee_members():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = firebase.post("/event_users", dataDict)
        return jsonify(result)
    return render_template('home.html')

## PUT REQUESTS
@app.route('/api/v1/edit_event', methods =['PUT'])
def add_event():
    return render_template('home.html')

@app.route('/api/v1/edit_user', methods =['PUT'])
def add_user():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = firebase.post("/users", dataDict)
        print(result)
        return jsonify(result)

    return redirect(url_for('index'))

@app.route('/api/v1/edit_location', methods =['PUT'])
def add_location():
    return render_template('home.html')

@app.route('/api/v1/edit_organisers', methods =['PUT'])
def add_committee_members():
    return render_template('home.html')

## DELETE REQUESTS
@app.route('/api/v1/delete_event', methods =['DELETE'])
def add_event():
    return render_template('home.html')

@app.route('/api/v1/delete_user', methods =['DELETE'])
def add_user():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = firebase.post("/users", dataDict)
        print(result)
        return jsonify(result)

    return redirect(url_for('index'))

@app.route('/api/v1/delete_location', methods =['DELETE'])
def add_location():
    return render_template('home.html')

@app.route('/api/v1/delete_organisers', methods =['DELETE'])
def add_committee_members():
    return render_template('home.html')

@app.route('/add_user_page')
def add_user_page():
	form = Add_user_form(request.form)
	return render_template('registration.html', form = form)

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
