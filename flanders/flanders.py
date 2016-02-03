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
DATABASE = 'flanders.db'
DEBUG = True
SECRET_KEY = 'development key'
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
        
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    sd = single_dic = {}
    fd = full_dic = {}
    if request.method == 'POST':
        user_id = int(random.random()*1000000000)
        user_id = str(user_id)
        for names in g.db.execute('select * from codepass'):
            sd['username'] = names[1]
            fd[str(names[0])] = sd
            sd = {}
        set_password = 0
        for item in fd:
            if request.form['username'] != fd[item]['username']:
                pass
            else:
                set_password = 1
        if set_password == 1:
            flash('Username Exists')
            error = 'User Exists'
            return redirect(url_for('register'))
        elif request.form['password'] != request.form['password_confirm']:
            flash('Password Does Not Match')
            error = 'Password Mismatch'
            return redirect(url_for('register'))
        else:
            print 'adding account'
            login = User(request.form['username'], request.form['password'])
            logins = pickle.dumps(login)
            not_reg = 0
            if request.form['position'] == 'employee':
                for names in g.db.execute('select * from payroll'):
                    if request.form['first_name'] == names[1] and request.form['last_name'] == names[2]:
                        g.db.execute('update payroll set userid=? where firstname=? and lastname=?', (user_id, names[1], names[2]))
                        g.db.execute('insert into register (position, firstname, lastname, emailaddr, userid, estid) values (?, ?, ?, ?, ?, ?)', [request.form['position'], request.form['first_name'], request.form['last_name'], request.form['email_addr'], user_id, request.form['est_id']])
                        g.db.execute('insert into codepass (username, password, userid) values (?, ?, ?)', [request.form['username'], logins, user_id])
                        g.db.commit()
                        not_reg = 0
                        return redirect(url_for('login'))
                    else:
                        not_reg = 1
                if not_reg == 1:
                    flash('Please Contact Your Manager')
            elif request.form['position'] == 'manager':
                g.db.execute('insert into register (position, firstname, lastname, emailaddr, userid, estid) values (?, ?, ?, ?, ?, ?)', [request.form['position'], request.form['first_name'], request.form['last_name'], request.form['email_addr'], user_id, request.form['est_id']])
                g.db.execute('insert into codepass (username, password, userid) values (?, ?, ?)', [request.form['username'], logins, user_id])
                g.db.commit()
                return redirect(url_for('login'))

    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    sd = single_dic = {}
    fd = full_dic = {}
    if request.method == 'POST':
        for names in g.db.execute('select * from codepass'):
            sd['username'] = names[1]
            sd['password'] = names[2]
            sd['userid'] = names[3]
            fd[str(names[0])] = sd
            sd = {}
        pass_error = 0
        user_error = 0
        for item in fd:
            if request.form['username'] == fd[item]['username']:
                if pickle.loads(fd[item]['password']).check_password(request.form['password']) == True:
                    pass_error = 0
                    session['logged_in'] = True
                    global user_id
                    user_id = fd[item]['userid']
                    return redirect(url_for('show_requests'))
                else:
                    pass_error = 1
            else:
                user_error = 1
        if user_error == 1 and pass_error != 1:
            flash('Username and Password is Incorrect')
        elif pass_error == 1:
            flash('Invalid Password Try Again!')
    cur = g.db.execute('select userid, startdate, starttime, requestsent, requestid, endtime, requestaccepted from requester order by id desc')
    requests = [dict(user_id=row[0], req_date=row[1], req_time=row[2], req_sent=row[3], req_id=row[4], end_time=row[5], req_accpt=row[6]) for row in cur.fetchall()]
    return render_template('show_requests.html', requests=requests, error=error)

@app.route('/', methods=['GET', 'POST'])
def show_requests():
    if request.method == 'POST':
        try:
            if request.form['cancelled'] == '1':
                g.db.execute('update brigade set brigadecancel=? where requestid=?', (1, request.form['cancel']))
                g.db.execute('update brigade set brigadeaccepted=? where requestid=?', (0, request.form['cancel']))
                g.db.execute('update requester set requestsent=? where requestid=?', (1, request.form['cancel']))
                g.db.execute('update requester set requestaccepted=? where requestid=?', (0, request.form['cancel']))
                g.db.commit()
                cur = g.db.execute('select userid, startdate, starttime, requestsent, requestid, endtime, requestaccepted from requester order by id desc')
                requests = [dict(user_id=row[0], req_date=row[1], req_time=row[2], req_sent=row[3], req_id=row[4], end_time=row[5], req_accpt=row[6]) for row in cur.fetchall()]
                return render_template('brigade.html', requests=requests)
        except:
            try:
                now = datetime.datetime.now()
                date = "%s/%s/%s" % (now.month, now.day, now.year)
                time = "%s:%s:%s" % (now.hour, now.month, now.second)
                g.db.execute('update requester set requestaccepted=? where requestid=?', (1, request.form['request']))
                g.db.execute('update requester set requestsent=? where requestid=?', (0, request.form['request']))
                g.db.execute('insert into brigade (requestid, brigadeid, accepteddate, acceptedtime, brigadeaccepted) values (?, ?, ?, ?, ?)', [request.form['request'], user_id, date, time, 1])
                g.db.commit()
                cur = g.db.execute('select userid, startdate, starttime, requestsent, requestid, endtime, requestaccepted from requester order by id desc')
                requests = [dict(user_id=row[0], req_date=row[1], req_time=row[2], req_sent=row[3], req_id=row[4], end_time=row[5], req_accpt=row[6]) for row in cur.fetchall()]
                return render_template('show_requests.html', requests=requests)
            except:
                return redirect(url_for('login'))
    else:                     
        #g.db.execute("DROP TABLE IF EXISTS register")
        #g.db.execute("DROP TABLE IF EXISTS profile")
        #g.db.execute("DROP TABLE IF EXISTS codepass")
        #g.db.execute("DROP TABLE IF EXISTS payroll")
        #g.db.execute("DROP TABLE IF EXISTS requester")
        #g.db.execute("DROP TABLE IF EXISTS brigade")
        #g.db.execute("DROP TABLE IF EXISTS profile")
        #g.db.execute("alter table profile add column '%s' 'integer'" % 'userid')
        cur = g.db.execute('select userid, startdate, starttime, requestsent, requestid, endtime, requestaccepted from requester order by id desc')
        requests = [dict(user_id=row[0], req_date=row[1], req_time=row[2], req_sent=row[3], req_id=row[4], end_time=row[5], req_accpt=row[6]) for row in cur.fetchall()]
        try:
            return render_template('show_requests.html', requests=requests, user_id=user_id)
        except:
            return render_template('show_requests.html', requests=requests)

    
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    error = None
    nl = name_list = []
    sd = single_dic = {}
    fd = full_dic = {}
    if request.method == 'POST':
            est_id = int(random.random()*1000000000)
            est_id = str(est_id)
            try:
                if request.form['regest'] == "1":
                    for items in g.db.execute('select * from profile'):
                        sd['est_company'] = items[1]
                        fd[str(items[0])] = sd
                        sd = {}
                        set_password = 0
                        for item in fd:
                            if request.form['est_company'] != fd[item]['est_company']:
                                pass
                            else:
                                set_password = 1
                        if set_password == 1:
                            flash('Company Exists')
                            error = 'Company Exists'
                            return redirect(url_for('profile'))
                        else:
                            flash('Share this id with your employees for registration\n'+est_id)
                            g.db.execute('insert into profile (company, address, city, state, zipcode, estid) values (?, ?, ?, ?, ?, ?)', [request.form['est_company'], request.form['est_address'], request.form['est_city'], request.form['est_state'], request.form['est_zip'], est_id])
                            g.db.execute('update register set estid=? where userid=?', (est_id, user_id))
                            g.db.commit()
                            return redirect(url_for('profile'))
            except:
                try:
                    if request.form['save'] == "1":
                        g.db.execute('update profile set callinternal=? where estid=?', (request.form['internal'], est_id))
                        g.db.execute('update profile set callnetwork=? where estid=?', (request.form['network'], est_id))
                        g.db.execute('update profile set callbrigade=? where estid=?', (request.form['brigade'], est_id))
                        g.db.commit()
                        return redirect(url_for('profile'))
                except:
                    try:
                        if request.form['upld'] == "1":
                            file = request.files['file']
                            if file and allowed_file(file.filename):
                                filename = secure_filename(file.filename)
                                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                                with open(UPLOAD_FOLDER+filename) as csvfile:
                                    dp = data_parse = csv.DictReader(csvfile)
                                    for row in dp:
                                        #ADD EST_ID INSERT TO DATABASE 
                                        g.db.execute('insert into payroll (firstname, lastname, eligible, active) values (?, ?, ?, ?)', [row['first_name'], row['last_name'], row['eligible'], row['active']])
                                        g.db.commit()
                                    flash('File Successfully Uploaded')
                                return redirect(url_for('profile'))
                    except:
                        flash('Error Saving')
    return render_template('profile.html', error=error)
    
UPLOAD_FOLDER = '/home/daniel/Daniel/dev/flask/flanders/app/data/upload/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    error = None
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(UPLOAD_FOLDER+filename) as csvfile:
                dp = data_parse = csv.DictReader(csvfile)
                for row in dp:
                    #ADD EST_ID INSERT TO DATABASE 
                    g.db.execute('insert into payroll (firstname, lastname, eligible, active) values (?, ?, ?, ?)', [row['first_name'], row['last_name'], row['eligible'], row['active']])
                    g.db.commit()
                flash('File Successfully Uploaded')
            return redirect(url_for('upload_file'))
    return render_template('upload.html', error=error)
    

@app.route('/brigade', methods=['GET', 'POST'])
def brigade():
    error = None
    sd = single_dic = {}
    fd = full_dic = {}

    if request.method == 'POST':
        request_id = int(random.random()*1000000000)
        request_id = str(request_id)
        try:
            subbtn = request.form['sub_butt']
            now = datetime.datetime.now()
            date = "%s/%s/%s" % (now.month, now.day, now.year)
            time = "%s:%s:%s" % (now.hour, now.month, now.second)
        except:
            cancelreq = request.form['can_button']
            now = datetime.datetime.now()
            time = "%s:%s:%s" % (now.hour, now.month, now.second)
            g.db.execute('update requester set canceltime=? where requestid=?', (time, cancelreq))
            g.db.execute('update requester set cancelmin=? where requestid=?', (now.minute, cancelreq))
            g.db.execute('update requester set requestcancel=? where requestid=?', (1, cancelreq))
            g.db.execute('update requester set requestsent=? where requestid=?', (0, cancelreq))
            g.db.commit()
        try:
            if cancelreq:
                return redirect(url_for('brigade'))
        except:
            g.db.execute('insert into requester (requestid, userid, requestsent, crntdate, crnttime, startdate, starttime, endtime, requestmin) values (?, ?, ?, ?, ?, ?, ?, ?, ?)', [request_id, user_id, 1, date, time, request.form['brigade_date'], request.form['brigade_time'], request.form['end_time'], now.minute])
            g.db.commit()
            return render_template('brigade.html', error=error, subbtn=subbtn, request_id=request_id)
    cur = g.db.execute('select userid, startdate, starttime, requestsent, requestid, endtime, requestaccepted from requester order by id desc')
    requests = [dict(user_id=row[0], req_date=row[1], req_time=row[2], req_sent=row[3], req_id=row[4], end_time=row[5], req_accpt=row[6]) for row in cur.fetchall()]
    return render_template('brigade.html', error=error, requests=requests, user_id=user_id)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_requests'))

if __name__ == '__main__':
    app.run()