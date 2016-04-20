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

DEBUG = True

#Local DB
client = MongoClient()
#Database Table Called Gorilla
db = client.mysite
#Database Collection
projects_db = db.projects
comments_db = db.comments
#Drop Database Table
#client.drop_database('mysite')

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

@app.route('/projects')
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run()
