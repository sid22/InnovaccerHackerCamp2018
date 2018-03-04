from flask import Flask
from flask import jsonify,make_response
from flask import request

import json
import tweepy

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)