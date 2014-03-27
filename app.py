from flask import Flask

app = Flask(__name__)
app.debug = True

from wpsc.cache import redis, redis_key
from wpsc.views import *

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8228)