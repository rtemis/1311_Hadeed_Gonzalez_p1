import os
import sys
import json
import random
import hashlib
import datetime
from flask import Flask, render_template, request, url_for, session, redirect
import unicodedata
from flask_session import Session


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

try:
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_NAME = 'flasksessionid'
    app.config.from_object(__name__)
    Session(app)
    print >>sys.stderr, "Usando sesiones de Flask-Session en fichero del servidor"
except ImportError as e:
    print >>sys.stderr, "Flask-Session no disponible, usando sesiones de Flask en cookie"

vacio = False

def setusername(username):
	global user
	user=True
	global session
	session['username'] = username	
	

def getusername():
	return session.get('username')

def getuser():
	return user

def setcart():
	global vacio
	vacio = True
	global session
	session['cart'] = []
	session['contador']={}

def addcart(movie):
	global session
	if movie in session['cart']:
		session['contador'][movie['titulo']] +=1
	else:
		session['cart'].append(movie)
		session['contador'][movie['titulo']]=1

def delcart(movie):
	global session
	if session['contador'][movie['titulo']] == 1:
		session['cart'].remove(movie)
		session['contador'].pop(movie['titulo'])
	else:
		session['contador'][movie['titulo']] -=1

def cleancart():
	global session
	session.pop('cart')
	session.pop('contador')
	global vacio
	vacio = False

def getcart():
	return session.get('cart')

def getcontador():
	return  session['contador']

@app.route("/*")
def logout():
	global user
	user=False
	global session
	session.clear()
	setcart()
	vacio = False
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
	if vacio == False:
		setcart()
	cart=getcart()
	leng = len(cart)
	contador=getcontador()

	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		movies = []
		for i in range(0,5):
			movies.append(random.choice(catalogue['peliculas']))
	return render_template('cart.html', title="Cart", username=username, user=getuser(), cart=cart, leng=leng, movies=movies, contador=contador)



@app.route("/add_to_cart", methods=['POST','GET'])
def add_to_cart():
	title=request.args.get('pelicula')

	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		for x in catalogue['peliculas']:
			if x['titulo'] == title:
				if vacio == False:
					setcart()
				addcart(x)
	return redirect(url_for('cart'))

@app.route("/remove", methods=['POST','GET'])
def remove_selected():
	peli=request.args.get('peli')
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		for x in catalogue['peliculas']:
			if x['titulo'] == peli:
				delcart(x)
	

	return redirect(url_for('cart'))


@app.route("/buy", methods=['POST', 'GET'])	
def buy_now():
	username=getusername()
	cart=getcart()
	contador = getcontador()
	dinero = 0
	historial= {}
	historial['peliculas']= []
	pelicula={}

	for x in cart:
		dinero += float(x['precio'])	


	with open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'r') as f:
		for line in f:
			parts = line.split(' : ')
				
			if  dinero <= parts[6]:
				for x in cart:
					pelicula['titulo']=x['titulo']
					pelicula['cantidad']=contador[x['titulo']]
			
					historial['peliculas'].append(pelicula)
							
		
	with open(os.path.join(app.root_path,'users/'+username+'/history.json'), 'a') as j:
		json.dump(historial, j)
	
	cleancart()

	return redirect(url_for('index'))

			

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
		open(os.path.join(app.root_path,'users/'+username+'/history.json'), 'w')
	
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
				if busqueda.lower() in x['titulo'].lower():
					movies.append(x)
	username = str(getusername())
	return render_template('results.html', title="Results", movies=movies, username=username, user=getuser())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
