import pickle

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from werkzeug.security import generate_password_hash, \
     check_password_hash
     
from werkzeug import secure_filename
from pymongo import MongoClient

client = MongoClient()
db = client.power
login_db = db.db_login

# create our little application :)
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

status = {'login':False,'admin':False}
    
@app.route('/', methods=['GET', 'POST'])
def index():
    login_status = False
    admin = False
    if request.method == 'POST':
        credentials = login_db.find(
            {
                "username": request.form['username'],
            }
        )
            
        for credential in credentials:
            username = credential['username']
            password = credential['password']
            account = credential['account']
            
        if password == request.form['password']:
            status['login'] = True
        if account == 'admin':
            status['admin'] = True
        return render_template('home.html',login_status=status['login'],admin=status['admin'])

    return render_template('home.html',login_status=status['login'],admin=status['admin'])

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        login_db.insert_one(
            {
                "username": request.form["basic-username"],
                "password": request.form["basic-password"],
                "account": "basic"
            }
        )
        return render_template('home.html',login_status=status['login'],admin=status['admin'])
    return render_template('admin.html',login_status=status['login'],admin=status['admin'])

@app.route('/superadmin', methods=['GET', 'POST'])
def superadmin():
    if request.method == 'POST':
        login_db.insert_one(
            {
                "username": request.form["super-username"],
                "password": request.form["super-password"],
                "account": "admin"
            }
        )
        return render_template('superadmin.html',login_status=status['login'],admin=status['admin'])
    return render_template('superadmin.html',login_status=status['login'],admin=status['admin'])

if __name__ == '__main__':
    app.run()