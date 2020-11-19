from flask import Flask
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'test key for flasklogin'
login_manager = LoginManager()
login_manager.init_app(app)


from flaskr import routes
