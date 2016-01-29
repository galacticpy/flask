from flask import Flask

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'dev key'#staging

from app import views