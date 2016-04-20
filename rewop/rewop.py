import powerpost
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# create our little application :)
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            api_key = request.form['pr-key']
            merchant = request.form['pr-merchant']        
            page_id = request.form['pr-pageid']
            resp = powerpost.postApi(api_key,merchant,page_id)
            return render_template('home.html', response=resp)
        except:
            return render_template('home.html')
    return render_template('home.html')

if __name__ == '__main__':
    app.run()