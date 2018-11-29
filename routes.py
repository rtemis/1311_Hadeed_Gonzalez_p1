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


vacio = False
buysuccess = 0
cookiexists = False
anno = 0
user = False

###############################s
# Funciones de session - user #
###############################
def setusername(username, customerid):
    global user
    user=True
    global session
    session['username'] = username
    session['customerid'] = customerid
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

def getcustomerid():
	return session.get('customerid')

def getusername():
	return session.get('username')

def getuser():
    global user
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
        session['contador'][movie[3]] +=1
    else:
        session['cart'].append(movie)
        session['contador'][movie[3]]=1

def delcart(movie):
    global session
    if session['contador'][movie[3]] == 1:
        session['cart'].remove(movie)
        session['contador'].pop(movie[3])
    else:
        session['contador'][movie[3]] -=1

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
    global anno
    anno = datetime.date.today().year-2
    global topVentas
    topVentas  = database.db_getTopVentas(anno)

    if buysuccess == 1:
        message = 1
    elif buysuccess == 2:
        message = 2

    c = getcookie()
    username = str(getusername())
    catalogue = database.db_catalogue()

    buysuccess = 0
    genres = database.db_genres()
    return render_template('index.html', title="Index", catalogue=catalogue, username=username, user=getuser(), loginsuccess = True, message=message, cookie = c, topVentas=topVentas, anno=anno, genres=genres)

######################
# Paginas de Session #
######################
@app.route("/~", methods=['POST', 'GET'])
def user():
    c = getcookie()
    username = request.form['username']
    password = request.form['password']
    global anno
    global topVentas
    topVentas  = database.db_getTopVentas(anno)

    loginsuccess = database.db_login(username, password)

    if loginsuccess == True:
        customerid = database.db_getCustomerid(username)
        setusername(username, customerid)


    catalogue = database.db_catalogue()
    genres = database.db_genres()
    return render_template('index.html', title="Index", catalogue=catalogue, username=username, user=getuser(), loginsuccess = loginsuccess,  message=0, cookie=c, topVentas=topVentas, anno=anno, genres=genres)

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
@app.route("/description/", methods=['GET', 'POST'])
def description():
    c = getcookie()
    movieid = request.args.get('movieid')
    title = request.args.get('title')

    mdetails = database.db_getDetails(movieid)
    long=len(mdetails[0][0])
    mdetails.append(movieid)

    username = str(getusername())
    genres = database.db_genres()
    return render_template('description.html', title=title, username=username, user=getuser(), loginsuccess = True, message=0, cookie=c, mdetails=mdetails, long=long, genres=genres)

#####################
# Paginas de Compra #
#####################
@app.route("/cart", methods=['POST', 'GET'])
def cart():
    #mostrar carro dependiendo de lgoueado o no
    c = getcookie()
    username = getusername()
    if vacio == False:
        setcart()
    if username == None:
        cart=getcart()

    else:
        customerid = getcustomerid()
        cart = getcart()
        if cart != None:
            for x in cart:
                prodid=x[3]
                contador = getcontador()
                for i in range(0,contador[prodid]):
                    database.db_addToCart(customerid, prodid)
            cleancart()
        cart = database.db_getCart(customerid)

    leng = len(cart)
    contador=getcontador()
    catalogue = database.db_catalogue()
    movies = []
    for i in range(0,5):
        movies.append(random.choice(catalogue))
    genres = database.db_genres()
    return render_template('cart.html', title="Cart", username=username, user=getuser(), cart=cart, leng=leng, movies=movies, contador=contador, loginsuccess = True, message=0, cookie=c, genres=genres)

@app.route("/add_to_cart", methods=['POST','GET'])
def add_to_cart():

	movieid=request.args.get('pelicula')
	price=request.form['price']

	username = getusername()
	#usuario no logueado
	if username == None:
		print username
		if vacio == False:
			print 'False'
			setcart()
		movie=database.db_getMovie(movieid)
		movie.append(price)
		prod_id=database.db_getProductId(movieid, price)
		movie.append(prod_id)
		addcart(movie)
	#usuario logueado
	else:
		prodid=database.db_getProductId(movieid, price)
		customerid=getcustomerid()
		database.db_addToCart(customerid, prodid)

		cart = getcart()
		if cart != None:
			for x in cart:
				prodid=x[3]
				contador = getcontador()
				for i in range(0,contador[prodid]):
					database.db_addToCart(customerid, prodid)
		cleancart()

	return redirect(url_for('cart'))

@app.route("/remove", methods=['POST','GET'])
def remove_selected():
    username = getusername()
    customerid=getcustomerid()

    movieid=request.args.get('peli')
    price = request.args.get('price')

    prod_id=database.db_getProductId(movieid, price)
    #usuario no logueado
    if username == None:
        movie=database.db_getMovie(movieid)
        movie.append(price)
        movie.append(prod_id)
        delcart(movie)
    else:
        database.db_removeFromCart(customerid, prod_id)

    return redirect(url_for('cart'))

@app.route("/buy", methods=['POST', 'GET'])
def buy_now():
    username=getusername()
    customerid = getcustomerid()
    cart=database.db_getCart(customerid)
    dinero = 0
    datos = {}
    datos['compras']=[]
    global buysuccess

    dinero = database.db_geTotalAmount(customerid)
    saldo = database.db_getCustomerIncome(customerid)

    if  float(dinero) <= float(saldo):
        variable = {}
        variable['date']= time.strftime("%x")
        variable['peliculas'] = []
        for x in cart:
            pelicula={}
            pelicula['titulo']=x[1]
            pelicula['cantidad']=x[4]
            pelicula['precio']=str(x[2])
            variable['peliculas'].append(pelicula)

        variable['precio'] = str(dinero)
        datos['compras'].append(variable)

        if 	os.path.isfile(os.path.join(app.root_path,'users/'+username+'/history.json')) == True:
            with open(os.path.join(app.root_path,'users/'+username+'/history.json'), 'r') as data:
                catalogue = {}
                catalogue = json.load(data)
                for x in catalogue['compras']:
                    datos['compras'].append(x)

        with open(os.path.join(app.root_path,'users/'+username+'/history.json'), 'w') as j:
            json.dump(datos, j)

        buysuccess = 1
        database.db_buy(customerid, dinero)

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
    customerid = getcustomerid()
    saldo = database.db_getCustomerIncome(customerid)
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

    genres = database.db_genres()
    return render_template('purchase-history.html', title="Purchase History",username=username, user=getuser(), history=history, existe=existe, movies=movies, loginsuccess = True, message=0, saldo = saldo, cookie=c, genres=genres)

#######################
# Incrementar Saldo #
#######################
@app.route("/history/i", methods=['POST','GET'])
def increase():
    customerid = getcustomerid()
    money = request.form['money']
    money=float(money)

    database.db_increaseIncome(customerid, money)
    return redirect(url_for('history'))


#######################
# Crear Nuevo Usuario #
#######################
@app.route("/register")
def register():
	c = getcookie()
	username = str(getusername())
	genres = database.db_genres()
	return render_template('register.html', title="Register",username=username, user=getuser(), loginsuccess = True, message=0, cookie=c, genres=genres)

@app.route("/new_user", methods=['POST'])
def user_test():
    c = getcookie()
    Fname = request.form['FnameField']
    Lname = request.form['LnameField']
    age = request.form['ageField']
    address1 = request.form['address1Field']
    address2 = request.form['address2Field']
    city = request.form['cityField']
    state = request.form['stateField']
    country = request.form['countryField']
    region = request.form['regionField']
    zip = request.form['zipField']
    gender = request.form['gender']
    if gender == 'male':
        gender = 'M'
    elif gender == 'female':
        gender = 'F'
    else:
        gender = 'O'
    username = request.form['usernameField']
    password = request.form['passwordField']
    email = request.form['emailField']
    phone = request.form['phoneField']
    creditcard = request.form['creditcardField']
    creditcardtype = request.form['creditcardtypeField']
    exMonth = request.form['exMonth']
    exYear = request.form['exYear']
    creditcardexp = str(exMonth)+'/'+str(exYear)

    registry = False
    password = hashlib.md5(password).hexdigest()
    registry = database.db_register(Fname, Lname, age, address1,address2, city, state, country, region, zip, gender, email, phone, creditcard, creditcardtype, creditcardexp, username, password)

    catalogue = database.db_catalogue()
    movies = []
    for i in range(0,5):
        movies.append(random.choice(catalogue))
    #De momento dejamos esta linea para que el hisotrial no explote
    if not os.path.isdir(os.path.join(app.root_path,'users/'+username+'/')):
        os.makedirs(os.path.join(app.root_path,'users/'+username+'/'), 0777)

    genres = database.db_genres()
    return render_template('user_test.html', registry=registry, movies=movies,username=username, user=getuser(), loginsuccess = True, message=0, cookie=c, genres=genres)

#########################
# Busqueda de Peliculas #
#########################
@app.route("/results", methods=['POST'])
def results():
    c = getcookie()
    genero = request.form['select']
    busqueda = request.form['search']

    movies = database.db_search(busqueda, genero)

    username = str(getusername())
    genres = database.db_genres()
    return render_template('results.html', title="Results", movies=movies, username=username, user=getuser(), loginsuccess = True, message=0, cookie=c, genres=genres)

@app.route("/hits", methods=['POST'])
def hits():
	return str(random.choice(range(1,1000)))

########
# Main #
########
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
