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
DATABASE = 'marge.db'
DEBUG = True
SECRET_KEY = 'templateunlock'
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
def index():
    return render_template('home.html')
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        maxid = g.db.execute('SELECT max(id) FROM edits')
        max_id = maxid.fetchone()[0]
        g.db.execute('update edits set active=? where id=?', (0,max_id))
        g.db.commit()
        g.db.execute('insert into edits (content, active) values (?,?)', [request.form['update-html'],1])        
        minid = g.db.execute('SELECT min(id) FROM edits')
        rows = g.db.execute('SELECT count(*) FROM edits')
        min_id = minid.fetchone()[0]
        count = rows.fetchone()[0]
       
        if count > 9:
            remove_id = min_id + 4
            while remove_id != min_id:
                g.db.execute('delete from edits where id='+str(remove_id))
                remove_id-=1
            g.db.execute('delete from edits where id='+str(min_id))
        g.db.commit()
        

        get = g.db.execute('select content, active from edits order by id desc')
        editdata = [dict(content=row[0], active=row[1]) for row in get.fetchall()]
        return render_template('edit.html', datas=editdata)
    try:
        get = g.db.execute('select content, active from edits order by id desc')
        editdata = [dict(content=row[0], active=row[1]) for row in get.fetchall()]
        return render_template('edit.html', datas=editdata)
    except:
        return render_template('edit.html')

@app.route('/services')
def services():
    return render_template('services.html')
@app.route('/projects')
def projects():
    return render_template('projects.html')
@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run()