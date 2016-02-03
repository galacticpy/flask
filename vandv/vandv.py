# all the imports
import sys
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = 'vandv.db'
DEBUG = True
SECRET_KEY = 'vandvunlock'
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
@app.route('/coolers')
def coolers():
    return render_template('coolers.html')
@app.route('/doors')
def doors():
    return render_template('doors.html')
@app.route('/equipment')
def equipment():
    return render_template('equipment.html')
@app.route('/demo')
def demo():
    return render_template('demolition.html')
@app.route('/residential')
def residential():
    return render_template('residential.html')
@app.route('/facades')
def facades():
    return render_template('facades.html')
@app.route('/clients')
def clients():
    return render_template('clients.html')
@app.route('/contactus')
def contactus():
    return render_template('contactus.html')
@app.route('/received', methods=['GET', 'POST'])
def received():
    if request.method == 'POST':
        g.db.execute('insert into received (name,email,comment) values (?, ?, ?)', [request.form['name'], request.form['email'], request.form['comments']])
        g.db.commit()
        flash('Successfully Submitted Comment')
    return render_template('contactus.html')


if __name__ == '__main__':
    app.run()