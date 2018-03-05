from flask import Flask
from flask import jsonify,make_response
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient

import json
# import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from datetime import datetime
import time
import re
import csv

#config details for twitter API calls by tweepy
consumer_key = "YmdoGWL3LRslmrNaGKieuIPZb"
consumer_secret =  "TMm1YkUjrzG5Cyj3h7HQpPX7TbTxLLxrtkfrOaA8RPXS3NBDLV"
access_token = "970413941800095744-vhZ8qkootBATVuhqUG6QbLM1CKps6fq"
access_token_secret = "MEFBREFJM5eFzp6Oiajiwq2HDkpFb5W5uwTvqrNKrFrwq"

app = Flask(__name__)

#Db part
app.config['MONGO_DBNAME'] = 'innovacer'
app.config['MONGO_URI'] = 'mongodb://jack:sparrow@ds012538.mlab.com:12538/innovacer'
mongo = PyMongo(app)

#Sample hello world part
@app.route('/')
def index():
   return "Hello, World!"

class StdOutListener(StreamListener):
  def __init__(self, time_limit=10):
    self.start_time = time.time()
    self.limit = time_limit
    super(StdOutListener, self).__init__()

  def on_data(self, data):
    if (time.time() - self.start_time) < self.limit:
    	try:
    		print "inside!"
	        user = mongo.db.users
	        tweet = mongo.db.tweets
	        datajson = json.loads(data)

	        #for user specific info, for the user who made the tweet.
	        uid = datajson['user']['id']
	        uname = datajson['user']['name']
	        uscreenname = datajson['user']['screen_name']
	        ulocation = datajson['user']['location']
	        ufollowers = datajson['user']['followers_count']  
	        ufriends = datajson['user']['friends_count']
	        user.insert_one({
		        "id": uid,
		        "name":uname,
		        "screen_name": uscreenname,
		        "location": ulocation,
		        "followers_count": ufollowers,
		        "friends_count": ufriends
		    })

	        #tweet data
	        tid = datajson['id']
	        trtwtcount = datajson['retweet_count']
	        tfavcount = datajson['favorite_count']
	        tcreate = datajson['created_at']
	        ttext = datajson['text']
	        tmention = datajson['entities']['user_mentions']
	        tweet.insert_one({
		        "id": tid,
		        "retweet_count": trtwtcount,
		        "fav_count": tfavcount,
		        "created_at": tcreate,
		        "text": ttext,
		        "mentions": tmention,
		    })
        except Exception as e:
        	print(e)
        
        return True

    #this else if for stopping the streaming, alternatively we can also return false in on_status
    else:
      return False

  def on_error(self, status):
        if (time.time() - self.time) >= self.limit:
            print 'time is over'
            return False
        else:
            print(status)
            return True



@app.route('/streamapi/<string:keyword>',methods=['POST'])
def stream_data(keyword):
   print "Keyword passed is:-" 
   print keyword
   auth = OAuthHandler(consumer_key, consumer_secret)
   auth.set_access_token(access_token, access_token_secret)

   st = StdOutListener()
   stream = Stream(auth, st)
   stream.filter(track=[keyword],languages=["en"])
   print "First API done!"
   response = {
		"code":"0","status":"success",
		"message":"Successful"
	}
	return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)