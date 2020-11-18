from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'test key for flasklogin'



from flaskr import routes
