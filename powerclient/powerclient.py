import pickle
import powerpost
import urllib2

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from werkzeug.security import generate_password_hash, \
     check_password_hash
     
from werkzeug import secure_filename
from pymongo import MongoClient
import urllib2


client = MongoClient()
db = client.power
login_db = db.db_login


#client.drop_database('power')
#db.drop_collection('db_login')

for item in login_db.find():
    print item

# create our little application :)
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

status = {'login':False,'account':'null', 'page_id':'null', 'merchant_group_id':'null', 'username':'null', 'client_url': False, 'review_url':'','valid_url':False, 'zip_location':'null'}
    
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
            merchant_group_id = credential['merchant_group_id']
            
        if password == request.form['password']:
            status['login'] = True
            try:
                status['username'] = username
                status['page_id'] = request.form['page_id']
                status['merchant_group_id'] = merchant_group_id
            except:
                pass
            status['account'] = account
        return render_template('home.html',login_status=status['login'],account=status['account'],merchant_group_id=merchant_group_id, page_id=status['page_id'], username=status['username'] )

    return render_template('home.html',login_status=status['login'],account=status['account'],merchant_group_id=status['merchant_group_id'], page_id=status['page_id'])

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        login_db.insert_one(
            {
                "username": request.form["basic-username"],
                "password": request.form["basic-password"],
                "merchant_group_id": request.form["merchant_group_id"],
                "account": "basic"
            }
        )
        return render_template('home.html',login_status=status['login'],account=status['account'])
    return render_template('admin.html',login_status=status['login'],account=status['account'])

@app.route('/superadmin', methods=['GET', 'POST'])
def superadmin():
    if request.method == 'POST':
        login_db.insert_one(
            {
                "username": request.form["super-username"],
                "password": request.form["super-password"],
                "merchant_group_id": 'null',
                "account": "admin"
            }
        )
        return render_template('superadmin.html',login_status=status['login'],account=status['account'])
    return render_template('superadmin.html',login_status=status['login'],account=status['account'])


@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        try:
            status['review_url'] = request.form['client_url']
            status['zip_location'] = request.form['zip_location']
            status['valid_url'] = True
            status['client_url'] = True
            return render_template('review.html',login_status=status['login'],account=status['account'],
                                   merchant_group_id=status['merchant_group_id'],zip_location=status['zip_location'],
                                   page_id=status['page_id'],review_url=status['review_url'],client_url=status['client_url'],
                                   valid_url=status['valid_url'])
        except:    
            status['page_id'] = request.form['page_id']
            try:
                status['merchant_group_id'] = request.form["merchant_group_id"]
            except:
                pass
            try:
                urllib2.urlopen('https://cdn.powerreviews.com/repos/'+status['merchant_group_id']+'/pr/pwr/engine/js/full.js')
                status['review_url'] = 'https://cdn.powerreviews.com/repos/'+status['merchant_group_id']+'/pr/pwr/engine/js/full.js'
                status['valid_url'] = True
                status['client_url'] = False
            except:
                status['valid_url'] = False
            return render_template('review.html',login_status=status['login'],account=status['account'],
                                   merchant_group_id=status['merchant_group_id'],page_id=status['page_id'],
                                   review_url=status['review_url'],client_url=status['client_url'],
                                   valid_url=status['valid_url'],zip_location=status['zip_location'])
    return render_template('review.html',login_status=status['login'],account=status['account'],
                           merchant_group_id=status['merchant_group_id'],page_id=status['page_id'],
                           review_url=status['review_url'],client_url=status['client_url'],
                           valid_url=status['valid_url'],zip_location=status['zip_location'])
    
@app.route('/apitester', methods=['GET', 'POST'])
def apitester():
    if request.method == 'POST':
        try:
            api_key = request.form['pr-key']
            merchant = request.form['pr-merchant']        
            page_id = request.form['pr-pageid']
            resp = powerpost.postApi(api_key,merchant,page_id)
            return render_template('apitester.html', response=resp, login_status=status['login'],account=status['account'])
        except:
            return render_template('apitester.html', login_status=status['login'],account=status['account'])
    return render_template('apitester.html', login_status=status['login'],account=status['account'])

@app.route('/war', methods=['GET', 'POST'])
def war():
    if request.method == 'POST':
        status['page_id'] = request.form['page_id']
        try:
            status['merchant_group_id'] = request.form["merchant_group_id"]
        except:
            pass
        return render_template('war.html',login_status=status['login'],account=status['account'],merchant_group_id=status['merchant_group_id'], page_id=status['page_id'])
    return render_template('war.html',login_status=status['login'],account=status['account'],merchant_group_id=status['merchant_group_id'], page_id=status['page_id'])


@app.route('/standalone')
def standalone():
    return render_template('standalone.html',login_status=status['login'])

@app.route('/logout')
def logout():
    status['login'] = False
    status['account'] = 'null'
    status['page_id'] = 'null'
    status['username'] = 'null'
    status['review_url'] = ''
    status['client_url'] = False
    status['valid_url'] = False
    status['merchant_group_id'] = 'null'
    status['zip_location'] = 'null'
    return render_template('home.html',login_status=status['login'],account=status['account'])

if __name__ == '__main__':
    app.run()
