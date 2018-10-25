import os
import sys
import json
import random
import hashlib
import datetime
from flask import Flask, render_template, request, url_for, session, redirect
import unicodedata


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

try:
    from flask_session import Session
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_NAME = 'flasksessionid'
    app.config.from_object(__name__)
    Session(app)
    print >>sys.stderr, "Usando sesiones de Flask-Session en fichero del servidor"
except ImportError as e:
    print >>sys.stderr, "Flask-Session no disponible, usando sesiones de Flask en cookie"



def setusername(username):
	global user
	user=True
	global session
	session['username'] = username	
	session['cart'] = []

def getusername():
	return session.get('username')

def getuser():
	return user

def setcart(movie):
	global session
	
	session['cart'].append(movie)

def getcart():
	return session.get('cart')

@app.route("/*")
def logout():
	global user
	user=False
	global session
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route("/")
def index():
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
	username = str(getusername())
	return render_template('index.html', title="Index", catalogue=catalogue, username=username, user=getuser())

@app.route("/~", methods=['POST', 'GET'])
def user():
	
	username = request.form['username']
	password = request.form['password']
	if  os.path.isdir(os.path.join(app.root_path,'users/'+username+'/')):
		for line in open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'r'):
			parts = line.split(' : ')
			if hashlib.md5(password).hexdigest() == parts[2] :
				setusername(username)

	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
			catalogue = {}
			catalogue = json.load(data)
	return render_template('index.html', title="Index", catalogue=catalogue, username=username, user=getuser())


@app.route("/description/<title>", methods=['GET'])
def description(title):
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		for x in catalogue['peliculas']:
			if x['titulo'] == title:
				movie = x

	username = str(getusername())
	return render_template('description.html', title=title, m=movie,username=username, user=getuser())

@app.route("/cart", methods=['POST', 'GET'])
def cart():
	username = str(getusername())
	cart=getcart()
	return render_template('cart.html', title="Cart", username=username, user=getuser(), cart=cart)

@app.route("/add_to_cart", methods=['POST','GET'])
def add_to_cart():
	username = str(getusername())
	title=request.args.get('pelicula')
	print title
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		for x in catalogue['peliculas']:
			if x['titulo'] == title:
				setcart(x)
	return redirect(url_for('cart'))

@app.route("/history")
def history():
	username = str(getusername())
	return render_template('purchase-history.html', title="Purchase History",username=username, user=getuser())

@app.route("/register")
def register():
	username = str(getusername())
	return render_template('register.html', title="Register",username=username, user=getuser())

@app.route("/new_user", methods=['POST'])
def user_test():
	name = request.form['nameField']
	username = request.form['usernameField']
	password = request.form['passwordField']
	email = request.form['emailField']
	creditcard = request.form['creditcardField']
	address = request.form['addressField']
	dob = request.form['birthdayField']
	registry = False
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		movies = []
		for i in range(0,5):
			movies.append(random.choice(catalogue['peliculas']))
	if not os.path.isdir(os.path.join(app.root_path,'users/'+username+'/')):
		os.makedirs(os.path.join(app.root_path,'users/'+username+'/'))
		registry = True
		with open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'w') as f:
			f.write(name + ' : ' + username +  ' : ' + hashlib.md5(password).hexdigest() + ' : ' + dob + ' : ' + address + ' : ' + creditcard + ' : ' + str(random.randint(1,101)))
		with open(os.path.join(app.root_path,'users/'+username+'/cart.json'), 'w+') as f:
			cart = {}
			cart['movies'] = []
			json.dump(cart, f)
	return render_template('user_test.html', registry=registry, movies=movies,username=username, user=getuser())

@app.route("/results", methods=['POST'])
def results():
	genero = request.form['select']
	busqueda = request.form['search']
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		movies = []
		if not busqueda:
			for x in catalogue['peliculas']:
				if genero in x['categoria']:
					movies.append(x)
		else:
			for x in catalogue['peliculas']:
				if x['titulo'].lower() == busqueda.lower():
					movies.append(x)
	username = str(getusername())
	return render_template('results.html', title="Results", movies=movies, username=username, user=getuser())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
