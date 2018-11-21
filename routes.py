import os
import time
import sys
import json
import random
import hashlib
import datetime
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, session
import unicodedata
import Cookie

import database

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

####################
# Setup de Session #
####################
try:
    from flask_session import Session
    this_dir = os.path.dirname(os.path.abspath(__file__))
    SESSION_FILE_DIR = this_dir + '/flask_session'
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_NAME = 'flasksessionid'
    app.config.from_object(__name__)
    Session(app)
    print >>sys.stderr, "Usando sesiones de Flask-Session en fichero del servidor"
except ImportError as e:
    print >>sys.stderr, "Flask-Session no disponible, usando sesiones de Flask en cookie"

conn = psycopg2.connect("host='localhost' dbname='si1' user='alumnodb' password='alumnodb'")

vacio = False
buysuccess = 0
cookiexists = False


###############################
# Funciones de session - user #
###############################
def setusername(username):
	global user
	user=True
	global session
	session['username'] = username
	global cookie
	cookie = Cookie.SimpleCookie()
	cookie['user'] = username
	global cookiexists
	cookiexists = True

def getcookie():
	if cookiexists == True:
		return str(cookie['user'].value)
	else:
		a = ""
		return a


def getusername():
	return session.get('username')

def getuser():
	return user

###############################
# Funciones de session - cart #
###############################
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
	setcart()

def getcart():
	return session.get('cart')

def getcontador():
	return  session['contador']

#########
# Index #
#########
@app.route("/")
def index():
	global buysuccess
	message = 0
	c = ""
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
	username = str(getusername())

	if buysuccess == 1:
		message = 1
	elif buysuccess == 2:
		message = 2

	c = getcookie()


	buysuccess = 0
	return render_template('index.html', title="Index", catalogue=catalogue, username=username, user=getuser(), loginsuccess = True, message=message, cookie = c)

######################
# Paginas de Session #
######################
@app.route("/~", methods=['POST', 'GET'])
def user():
	c = getcookie()
	loginsuccess = False
	username = request.form['username']
	password = request.form['password']
	if  os.path.isdir(os.path.join(app.root_path,'users/'+username+'/')):
		for line in open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'r'):
			parts = line.split(' : ')
			if hashlib.md5(password).hexdigest() == parts[2] :
				setusername(username)
				loginsuccess = True



	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
			catalogue = {}
			catalogue = json.load(data)
	return render_template('index.html', title="Index", catalogue=catalogue, username=username, user=getuser(), loginsuccess = loginsuccess,  message=0, cookie=c)

@app.route("/*")
def logout():
	global user
	user=False
	global session
	session.clear()
	setcart()
	vacio = False
	return redirect(url_for('index'))

###############
# Descripcion #
###############
@app.route("/description/<title>", methods=['GET'])
def description(title):
	c = getcookie()
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		for x in catalogue['peliculas']:
			if x['titulo'] == title:
				movie = x

	username = str(getusername())
	return render_template('description.html', title=title, m=movie,username=username, user=getuser(), loginsuccess = True, message=0, cookie=c)

#####################
# Paginas de Compra #
#####################
@app.route("/cart", methods=['POST', 'GET'])
def cart():
	c = getcookie()
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
	return render_template('cart.html', title="Cart", username=username, user=getuser(), cart=cart, leng=leng, movies=movies, contador=contador, loginsuccess = True, message=0, cookie=c)

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
	datos = {}
	datos['compras']=[]
	pelicula={}
	global buysuccess

	for x in cart:
		dinero += float(x['precio']*contador[x['titulo']])



	with open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'r') as f:
		for line in f:
			parts = line.split(' : ')
		saldo = float(parts[6])
		if  dinero <= saldo:
			precio = 0
			variable = {}
			variable['date']= time.strftime("%x")
			variable['peliculas'] = []
			for x in cart:

				pelicula['titulo']=x['titulo']
				pelicula['cantidad']=contador[x['titulo']]
				pelicula['precio']=x['precio']
				precio += (x['precio']*contador[x['titulo']])

				variable['peliculas'].append(pelicula)
				pelicula={}

			variable['precio'] = precio
			datos['compras'].append(variable)

			if 	os.path.isfile(os.path.join(app.root_path,'users/'+username+'/history.json')) == True:
				with open(os.path.join(app.root_path,'users/'+username+'/history.json'), 'r') as data:
						catalogue = {}
						catalogue = json.load(data)

						for x in catalogue['compras']:

							datos['compras'].append(x)


			with open(os.path.join(app.root_path,'users/'+username+'/history.json'), 'w') as j:

				json.dump(datos, j)

			cleancart()

			buysuccess = 1

			with open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'r') as f:
				parts = line.split(' : ')
				parts[6] = str(saldo-dinero)

			with open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'w') as f:
				f.write(parts[0] + ' : ' + parts[1] +  ' : ' + parts[2] + ' : ' + parts[3] + ' : ' +parts[4] + ' : ' + parts[5] + ' : ' + parts[6])

		else:
			buysuccess = 2



	return redirect(url_for('index'))

########################
# Paginas de Historial #
########################

@app.route("/history")
def history():
	c = getcookie()
	username = str(getusername())
	history={}
	existe=False
	if 	os.path.isfile(os.path.join(app.root_path,'users/'+username+'/history.json')) == True:
		existe=True
		with open(os.path.join(app.root_path,'users/'+username+'/history.json'), 'r') as data:

			history = json.load(data)

	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		movies = []
		for i in range(0,5):
			movies.append(random.choice(catalogue['peliculas']))

	with open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'r') as f:
		for line in f:
			parts = line.split(' : ')
			saldo=parts[6]

	return render_template('purchase-history.html', title="Purchase History",username=username, user=getuser(), history=history, existe=existe, movies=movies, loginsuccess = True, message=0, saldo = saldo, cookie=c)

#######################
# Incrementar Saldo #
#######################
@app.route("/history/i", methods=['POST','GET'])
def increase():
	username = str(getusername())
	money = request.form['money']

	with open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'r') as f:
		for line in f:
			parts = line.split(' : ')
		saldo= float(parts[6])+float(money)

	with open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'w') as f:
				f.write(parts[0] + ' : ' + parts[1] +  ' : ' + parts[2] + ' : ' + parts[3] + ' : ' +parts[4] + ' : ' + parts[5] + ' : ' + str(saldo))

	return redirect(url_for('history'))


#######################
# Crear Nuevo Usuario #
#######################
@app.route("/register")
def register():
	c = getcookie()
	username = str(getusername())
	return render_template('register.html', title="Register",username=username, user=getuser(), loginsuccess = True, message=0, cookie=c)

@app.route("/new_user", methods=['POST'])
def user_test():
	c = getcookie()
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
		os.makedirs(os.path.join(app.root_path,'users/'+username+'/'), 0777)
		registry = True
		with open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'w') as f:
			f.write(name + ' : ' + username +  ' : ' + hashlib.md5(password).hexdigest() + ' : ' + dob + ' : ' + address + ' : ' + creditcard + ' : ' + str(random.randint(1,101)))


	return render_template('user_test.html', registry=registry, movies=movies,username=username, user=getuser(), loginsuccess = True, message=0, cookie=c)

#########################
# Busqueda de Peliculas #
#########################
@app.route("/results", methods=['POST'])
def results():
	c = getcookie()
	genero = request.form['select']
	busqueda = request.form['search']
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		movies = []
		aux=[]
		if not busqueda:
			if genero != "#":
				for x in catalogue['peliculas']:
					if genero in x['categoria']:
						movies.append(x)
			else:
				movies=catalogue['peliculas']
		else:
			if genero != "#":
				for x in catalogue['peliculas']:
					if genero in x['categoria']:
						aux.append(x)


				for x in aux:
					if busqueda.lower() in x['titulo'].lower():
						movies.append(x)
			else:
				for x in catalogue['peliculas']:
					if busqueda.lower() in x['titulo'].lower():
						movies.append(x)

	username = str(getusername())


	return render_template('results.html', title="Results", movies=movies, username=username, user=getuser(), loginsuccess = True, message=0, cookie=c)

@app.route("/hits", methods=['POST'])
def hits():
	return str(random.choice(range(1,1000)))

########
# Main #
########
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
