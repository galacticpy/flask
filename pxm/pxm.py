# all the imports
import sys
import json
import os
import datetime
import pickle
import random
import csv
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from werkzeug.security import generate_password_hash, \
     check_password_hash
     
from werkzeug import secure_filename
from pymongo import MongoClient

#Heroku
MONGOLAB_URI = 'mongodb://heroku_500fpzjz:4jskk7nh6td45e8n4juhpnlfit@ds011912.mlab.com:11912/heroku_500fpzjz'
client = MongoClient(MONGOLAB_URI)

#Local DB
#client = MongoClient()
#Database
db = client.heroku_500fpzjz

#Database Collection
projects_db = db.projects
comments_db = db.comments
#Drop Database Tabless
#client.drop_database('pxm')

# create our little application :)
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')

@app.route('/codeofday')
def codeofday():
    return render_template('codeofday.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['contact-name']
        email = request.form['contact-email']
        comment = request.form['contact-comment']
        comments_db.insert_one(
            {
                "name": name,
                "email": email,
                "comment": comment,
            }
        )       
        return render_template('contact.html',name=name,email=email,comment=comment)
    return render_template('contact.html')

if __name__ == '__main__':
    app.run()
