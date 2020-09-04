from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import Mars_scrape
import os

STATIC_DIR=os.path.abspath('/static')
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_app")

@app.route("/")
def home():
    mars_data = mongo.db.mars.find_one()
    mars_table=pd.read_html('Mars_facts.html')
    return render_template("index.html",mars_data=mars_data,mars_table=mars_table)


@app.route('/scrape')
def scrape_mars():
    mars_data=Mars_scrape.scrape()
    mongo.db.mars.update({}, mars_data, upsert=True)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

