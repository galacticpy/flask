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

#Heroku
#MONGOLAB_URI = "mongodb://dkenned23:2308745dk@ds015508.mlab.com:15508/heroku_l74kqc7r"
#client = MongoClient(MONGOLAB_URI)

#Local DB
client = MongoClient()
#Database Table Called Gorilla
db = client.gorilla
#Database Collection
login_db = db.db_login
account_db = db.db_account
brigade_db = db.db_brigade
#Drop Database Table
#client.drop_database('gorilla')

class User(object):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

#Creates Password Hash
#login = User(request.form['username'], request.form['password'])
#logins = pickle.dumps(login)

#Checks if password matches hashed password
#if pickle.loads(fd[item]['password']).check_password(request.form['password']):


# create our little application :)
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

session = {}
session_id = int(random.random()*100000000000)
session_id = str(session_id)

account_data = {}
account_data['login'] = False
account_data['user_id'] = False

session[session_id] = account_data

@app.route('/', methods=['GET', 'POST'])
def index():
    x = brigade_db.find()
    for i in x:
        print i
    return render_template('home.html',
                           login_status=session[session_id]['login'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #flag for checking if the username already exists
        username_exists = False
        check_username = login_db.find(
            {
                "username": request.form["username-register"]
            }
        )
        for username_check in check_username:
            
            if request.form['username-register'] == username_check['username']:
                username_exists = True
    
        if not username_exists:
            user_id = int(random.random()*1000000000)
            user_id = str(user_id)
            account_data['user_id'] = user_id
            session[session_id] = account_data
            #Add Document to names Collection
            login_db.insert_one(
                {
                    "user_id": session[session_id]['user_id'],
                    "username": request.form["username-register"],
                    "password": request.form["password-register"]
                }
            )
            account_db.insert_one(
                {
                    "user_id": session[session_id]['user_id'],
                    "first_name": request.form["first_name"],
                    "last_name": request.form["last_name"],
                    "email_address": request.form["email_address"],
                }
            )
            #Find name document in names Collection
            credentials = login_db.find(
                {
            "user_id": session[session_id]['user_id'],
                }
            )
    
            names = account_db.find(
                {
                    "user_id": session[session_id]['user_id'],
                }
            )
            
            for credential in credentials:
                username = credential['username']
                password = credential['password']
                userid = credential['user_id']
            
            for name in names:
                firstname = name['first_name']
                lastname = name['last_name']
                email = name['email_address']
            
            return render_template('register.html',
                                   registered=True)
                
        else:
            return render_template('register.html',
                                   username_exists=username_exists)

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        validate_password = login_db.find(
            {
                "username": request.form["username-login"]
            }
        )
        for password in validate_password:
            if request.form['password-login'] == password['password']:
                account_data['login'] = True
                account_data['user_id'] = password['user_id']
                session[session_id] = account_data
                username=password['username']
                return render_template('home.html',
                                       username=username,
                                       login_status=session[session_id]['login'])
            
            else:
                account_data['login'] = False
                return render_template('register.html',
                                       invalid_password=True,
                                       login_status=session[session_id]['login'])
            
    return render_template('register.html',
                           login_status=session[session_id]['login'])

@app.route('/account', methods=['GET', 'POST'])
def account():
    if session[session_id]['login']:
        login_status = session[session_id]['login']
        my_account = account_db.find(
            {
            "user_id": session[session_id]['user_id'],
            }
        )
        my_credentials = login_db.find(
            {
            "user_id": session[session_id]['user_id'],
            }
        )

        for info in my_account:
            firstname = info['first_name']
            lastname = info['last_name']
            email = info['email_address']
        
        for info in my_credentials:
            username = info['username']
            password = info['password']
            userid = info['user_id']
            
        if request.method == 'POST':
            dropdown_options = {"0":"","1":"Sports Bars", "2":"Pub"}
            dropdown_option = request.form['mantis-option']
            mantis_option = dropdown_options[dropdown_option]
            return render_template('account.html',
                                   firstname=firstname,
                                   lastname=lastname, username=username,
                                   password=password, userid=userid, email=email,
                                   mantis_option=mantis_option,
                                   login_status=login_status)

        else:
            return render_template('account.html',
                                   firstname=firstname,
                                   lastname=lastname, username=username,
                                   password=password, userid=userid, email=email,
                                   login_status=login_status)

    else:
        return render_template('register.html')

@app.route('/brigade_request', methods=['GET', 'POST'])
def brigade_request():
    brigade_request_post = False
    if session[session_id]['login']:
        if request.method == 'POST':
            brigade_request_post = True
            brigade_id = int(random.random()*1000000000)
            brigade_id = str(brigade_id)
            brigade_date = request.form["brigade-date"]
            brigade_starttime = request.form["brigade-starttime"]
            brigade_endtime = request.form["brigade-endtime"]
            brigade_db.insert_one(
                {
                    "brigade_id": brigade_id,
                    "brigade_date": brigade_date,
                    "brigade_start_time": brigade_starttime,
                    "brigade_end_time": brigade_endtime,
                    "brigade_status": "False",
                    "brigade_requester_id": session[session_id]['user_id'],
                    "brigade_accepter_id": "False"
                }
            )
            return render_template('home.html',
                                   login_status=session[session_id]['login'],
                                   brigade_request_post=brigade_request_post,
                                   brigade_date=brigade_date,
                                   brigade_starttime=brigade_starttime,
                                   brigade_endtime=brigade_endtime)
        
        return render_template('home.html',
                               login_status=session[session_id]['login'],
                               brigade_request_post=brigade_request_post)
    
    return render_template('home.html', login_status=session[session_id]['login'],
                           brigade_request_post=brigade_request_post)

@app.route('/brigade', methods=['GET', 'POST'])
def brigade():
    brigade_post = False
    brigade_requests = brigade_db.find()
    if request.method == 'POST':
        sub = request.form["submit-brigade"]
        brigade_value = request.form["submit-brigade"].split('.', 1)[-1]
        brigade_id = str(sub).split('.')[0]
        brigade_post = True
        
        if brigade_value == "False":
            brigade_accepter_id = "False"
        else:
            brigade_accepter_id = session[session_id]['user_id']
            
        brigade_db.update_one(
            {"brigade_id": brigade_id},
            {"$set":
                {"brigade_accepter_id": brigade_accepter_id,
                "brigade_status": brigade_value}}
        )
        return render_template('brigade.html',
                               login_status=session[session_id]['login'],
                               brigade_post=brigade_post,
                               brigade_user_id=session[session_id]['user_id'])
    
    return render_template('brigade.html',
                           login_status=session[session_id]['login'],
                           brigade_post=brigade_post,
                           brigade_requests=brigade_requests,
                           brigade_user_id=session[session_id]['user_id'])
    

@app.route('/logout')
def logout():
    session[session_id]['login'] = False
    session[session_id]['user_id'] = False
    return render_template('register.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
