import os
import json
import random
import hashlib
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
	return render_template('index.html', title="Index", user=False, catalogue=catalogue)

@app.route("/~", methods=['POST'])
def user():
	username = request.form['username']
	password = request.form['password']
	user = False
	if  os.path.isdir(os.path.join(app.root_path,'users/'+username+'/')):
		for line in open(os.path.join(app.root_path,'users/'+username+'/datos.dat'), 'r'):
			parts = line.split(' : ')
			if hashlib.md5(password).hexdigest() == parts[3] :
				user = True	

	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
			catalogue = {}
			catalogue = json.load(data)
	
	return render_template('index.html', title="Index", user=user, catalogue=catalogue, username=username)

@app.route("/about")
def about():
	return render_template('about-us.html', title="About Us")

@app.route("/contact")
def contact():
	return render_template('contact-us.html', title="Contact Us")

@app.route("/description/<title>", methods=['GET'])
def description(title):
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		catalogue = {}
		catalogue = json.load(data)
		for x in catalogue['peliculas']:
			if x['titulo'] == title:
				movie = x

	return render_template('description.html', title=title, m=movie)

@app.route("/cart")
def cart():
	return render_template('cart.html', title="Cart")

@app.route("/history")
def history():
	return render_template('purchase-history.html', title="Purchase History")

@app.route("/register")
def register():
	

	return render_template('register.html', title="Register")

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
			f.write(name + ' : ' + username + ' : ' + password + ' : ' + hashlib.md5(password).hexdigest() + ' : ' + dob + ' : ' + address + ' : ' + creditcard + ' : ' + str(random.randint(1,101)))
	return render_template('user_test.html', registry=registry, movies=movies)

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
	return render_template('results.html', title="Results", movies=movies)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
