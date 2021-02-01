from flask import Flask
from twython import Twython
from datetime import timezone, timedelta

import config

DEBUG = config.DEBUG
CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
ACCESS_KEY = config.ACCESS_KEY
ACCESS_SECRET = config.ACCESS_SECRET

# setup for twython
twitter = Twython(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_KEY,
    ACCESS_SECRET
)

# setup for flask
app = Flask(__name__, template_folder='../dist', static_folder='../dist/static')
app.debug = DEBUG

# jst
jst = timezone(timedelta(hours=+9), 'JST')

# import other script
import src.views
