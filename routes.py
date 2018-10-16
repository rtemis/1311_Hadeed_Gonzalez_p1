import os
import json
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

@app.route("/results", methods=['GET']) 
def results():
	genre = request.args.get("select")
	busqueda = request.args.get("search")
	with open(os.path.join(app.root_path,'catalogue/catalogue.json'), 'r') as data:
		movies = {}
		movies = json.load(data)	
	return render_template('results.html', title="Results", movies=movies, genre=genre, busqueda=busqueda)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
