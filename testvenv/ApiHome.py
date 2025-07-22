import flask
from flask import Flask,render_template
import json
import pymongo
from pymongo import MongoClient


app = Flask(__name__)
##client = pymongo.MongoClient("mongodb+srv://rakeshvasal:pass123456@rakesh1-9x2sl.gcp.mongodb.net/test?retryWrites=true")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

db = myclient["mydatabase"]
##db = client['TestDB']
user_collection = db['users']
event_collection = db['events']
organisers_collection = db['organisers']
location_collection = db['locations']

@app.route('/')
def index():
    collection = db['FirstCollection']
    print(collection.find_one())
    collist = db.list_collection_names()
    mydict = { "name": "John", "address": "Highway 37" }
    x = collection.insert_one(mydict)
    print(x)
    if "FirstCollection" in collist:
        print("The collection exists.")
    return render_template('home.html')

## GET REQUESTS
@app.route('/api/v1/get_users', methods=['GET'])
def get_all_users():
    userdata = ''
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

################################### POST REQUESTS ##########################################
@app.route('/api/v1/add_event', methods =['POST'])
def add_event():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = event_collection.insert_one(dataDict)
        return jsonify(result)
    return redirect(url_for('index'))

@app.route('/api/v1/add_user', methods =['POST'])
def add_user():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = user_collection.insert_one(dataDict)
        return jsonify(result)
    return redirect(url_for('index'))

@app.route('/api/v1/add_location', methods =['POST'])
def add_location():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = location_collection.insert_one(dataDict)
        return jsonify(result)
    return render_template('home.html')

@app.route('/api/v1/add_organisers', methods =['POST'])
def add_committee_members():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = organisers_collection.insert_one(dataDict)
        return jsonify(result)
    return render_template('home.html')

###################################### PUT REQUESTS ##########################################
@app.route('/api/v1/edit_event', methods =['PUT'])
def edit_event():
    return render_template('home.html')

@app.route('/api/v1/edit_user', methods =['PUT'])
def edit_user():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = firebase.post("/users", dataDict)
        print(result)
        return jsonify(result)

    return redirect(url_for('index'))

@app.route('/api/v1/edit_location', methods =['PUT'])
def edit_location():
    return render_template('home.html')

@app.route('/api/v1/edit_organisers', methods =['PUT'])
def edit_committee_members():
    return render_template('home.html')

######################################## DELETE REQUESTS #######################################
@app.route('/api/v1/delete_event', methods =['DELETE'])
def delete_event():
    return render_template('home.html')

@app.route('/api/v1/delete_user', methods =['DELETE'])
def delete_user():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        result = firebase.post("/users", dataDict)
        print(result)
        return jsonify(result)

    return redirect(url_for('index'))

@app.route('/api/v1/delete_location', methods =['DELETE'])
def delete_location():
    return render_template('home.html')

@app.route('/api/v1/delete_organisers', methods =['DELETE'])
def delete_organisers():
    return render_template('home.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
