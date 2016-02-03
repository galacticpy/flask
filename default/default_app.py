# all the imports
import sys
import os
import datetime
import sqlite3
import pickle
import random
import csv
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from werkzeug.security import generate_password_hash, \
     check_password_hash
     
from werkzeug import secure_filename

class User(object):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

# configuration
DATABASE = 'vandv.db'
DEBUG = True
SECRET_KEY = 'defaultunlock'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
@app.route('/')
def show_requests():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()