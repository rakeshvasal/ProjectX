import flask
from flask import Flask,render_template
from flask_pymongo import PyMongo
from firebase import firebase
import json

app = Flask(__name__)

app.config ['MONGO_DBNAME'] = 'localhost'
app.config ['MONGO_URI'] = 'mongodb://rakeshvasaldbadmin:rakeshvasal02@ds259912.mlab.com:59912/oddesseydb'

mongo = PyMongo(app)

firebase = firebase.FirebaseApplication('https://myapplication-8f68b.firebaseio.com/', None)

@app.route('/')
def index():
	user = mongo.db.users
	##user.insert({'name' : 'Rakesh'})
	userlist = []
	result = firebase.get('/users', None)
	for x, y in result.items():
		userdata = json.dumps(y)
		lastindex = userdata.rindex('}')
		userdata = userdata[:lastindex]
		userdata = userdata + " ,\"id\" : \"" + x + "\"}"
		data = json.loads(userdata)
		string = json.dumps(data)
		branch = data["branch"]
		##post_id = user.insert_one(data).inserted_id
		##print(post_id)

	return render_template('home.html')

@app.route('/migrateevents')
def migrateevents():
	event = mongo.db.events
	result = firebase.get('/events', None)
	for x, y in result.items():
		events = json.dumps(y)
		lastindex = events.rindex('}')
		events = events[:lastindex]
		events = events + " ,\"id\" : \"" + x + "\"}"
		data = json.loads(events)
		##post_id = event.insert_one(data).inserted_id
		##print(post_id)

	return render_template('home.html')

@app.route('/migratelocations')
def migratelocations():
	location = mongo.db.locations
	results = firebase.get('/locations',None)
	for x,y in results.items():
		locations = json.dumps(y)
		lastindex = locations.rindex('}')
		locations = locations[:lastindex]
		locations = locations + " ,\"id\" : \"" + x + "\"}"
		data = json.loads(locations)
		##post_id = location.insert_one(data).inserted_id
		##print(post_id)

	return render_template('home.html')

app.route('/eventusers')
def migrateeventusers():
	eventuser = mongo.db.event_users
	results = firebase.get('/event_users',None)
	for x,y in results.items():
		event_users = json.dumps(y)
		lastindex = event_users.rindex('}')
		event_users = event_users[:lastindex]
		event_users = event_users + " ,\"id\" : \"" + x + "\"}"
		data = json.loads(event_users)
		post_id = eventuser.insert_one(data).inserted_id
		print(post_id)

	return render_template('home.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
