import os
import json
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
	with open('catalogo.json', 'r') as data:
		catalogue = json.load(data)
		movies = {}
		for p in catalogue['peliculas']:
			movies['p.titulo'] = p['poster']	
	return render_template('index.html', title="Index", user=False)

@app.route("/about")
def about():
	return render_template('about-us.html', title="About Us")

@app.route("/contact")
def contact():
	return render_template('contact-us.html', title="Contact Us")

@app.route("/cart")
def cart():
	return render_template('cart.html', title="Cart")

@app.route("/history")
def history():
	return render_template('purchase-history.html', title="Purchase History")

@app.route("/register")
def register():
	return render_template('register.html', title="Register")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)