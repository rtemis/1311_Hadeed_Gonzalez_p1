import os
import sys
import json
import random
import hashlib
from flask import Flask, render_template, request, url_for, session, redirect

app = Flask(__name__)

try:
    from flask_session import Session
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_NAME = 'flasksessionid'
    app.config.from_object(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    Session(app)
    print >>sys.stderr, "Usando sesiones de Flask-Session en fichero del servidor"
except ImportError as e:
    print >>sys.stderr, "Flask-Session no disponible, usando sesiones de Flask en cookie"



def set(username):
	global user
	user=True
	global session
	session['username'] = username	

def get():
	return session.get('username')

def getuser():
	return user

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
	username = str(get())
	return render_template('index.html', title="Index", catalogue=catalogue, username=username, user=getuser())

@app.route("/~", methods=['POST', 'GET'])
def user():
	
	username = request.form['username']
	password = request.form['password']
	if  os.path.isdir(os.path.join(app.root_path,'users/'+username+'/')):
		for line in open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'r'):
			parts = line.split(' : ')
			if hashlib.md5(password).hexdigest() == parts[2] :
				set(username)

	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
			catalogue = {}
			catalogue = json.load(data)
	username = str(get())
	return render_template('index.html', title="Index", catalogue=catalogue, username=username, user=getuser())


@app.route("/description/<title>", methods=['GET'])
def description(title):
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		for x in catalogue['peliculas']:
			if x['titulo'] == title:
				movie = x
	username = str(get())
	return render_template('description.html', title=title, m=movie,username=username, user=getuser())

@app.route("/cart")
def cart():
	username = str(get())
	if not os.path.isdir(os.path.join(app.root_path,'users/'+username+'/cart.json')):
		with open(os.path.join(app.root_path, 'users/'+username+'/cart.json'), 'w')
	with open(os.path.join(app.root_path, 'users/'+username+'/cart.json'), 'r') as data:
		movies = {}
		movies = json.load(data)
	
	return render_template('cart.html', title="Cart", movies=movies,username=username, user=getuser())

@app.route("/history")
def history():
	username = str(get())
	return render_template('purchase-history.html', title="Purchase History",username=username, user=getuser())

@app.route("/register")
def register():
	username = str(get())
	return render_template('register.html', title="Register",username=username, user=getuser())

@app.route("/new_user", methods=['POST'])
def user_test():
	name = request.form['name']
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	creditcard = request.form['creditcard']
	address = request.form['address']
	dob = request.form['dob']
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
	
	username = str(get())
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
	username = str(get())
	return render_template('results.html', title="Results", movies=movies,username=username, user=getuser())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
