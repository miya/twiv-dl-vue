import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
