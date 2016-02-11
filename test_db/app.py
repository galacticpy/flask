from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_db'
db = SQLAlchemy(app)

# Create our database model
class Posts(db.Model):
    __tablename__ = "Posts"
    id = db.Column(db.Integer, primary_key=True)
    html = db.Column(db.Text(), unique=True)

    def __init__(self, html):
        self.html = html

    def __repr__(self):
        return '<Posts %r>' % self.html

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services', methods=['GET', 'POST'])
def services():
    if request.method == 'POST':
        html = request.form['html']
        reg = Posts(html)
        db.session.add(reg)
        db.session.commit()
        html = db.session.query(Posts)
        return render_template('services.html', html=html)
    try:
        html = db.session.query(Posts)
        return render_template('services.html', html=html)
    except:
        return render_template('services.html')


if __name__ == '__main__':
    app.debug = True
    app.run()