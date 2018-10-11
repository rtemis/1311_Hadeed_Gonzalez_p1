import os
import json
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
	with open('catalogo.json', 'r') as data:
		catalogue = {}
		catalogue = json.load(data)	
	return render_template('index.html', title="Index", user=False, catalogue=catalogue)

@app.route("/about")
def about():
	return render_template('about-us.html', title="About Us")

@app.route("/contact")
def contact():
	return render_template('contact-us.html', title="Contact Us")

@app.route("/<title>")
def description(movie):
	return render_template('description.html', title='movie["titulo"]', movie=m)

@app.route("/cart")
def cart():
	return render_template('cart.html', title="Cart")

@app.route("/history")
def history():
	return render_template('purchase-history.html', title="Purchase History")

@app.route("/register")
def register():
	return render_template('register.html', title="Register")

@app.route("/results", methods=['GET']) 
def results():
	genero = request.form['select']
	busqueda = request.form['search']
	with open('catalogo.json', 'r') as data:
		catalogue = {}
		catalogue = json.load(data)	
		moviebase = {}
		movies = {}
		for p in catalogue.peliculas:
			if genero in p.categoria:
				moviebase[genero] = p
		for p in moviebase:
			if p.titulo.lower().contains(busqueda.lower()):
				movies[p.titulo] = p
	return render_template('results.html', title="Results", movies=movies)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)