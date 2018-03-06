from flask import Flask
from flask import jsonify,make_response
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient

import json
from bson import json_util
from bson import Binary, Code
from bson.json_util import dumps

# import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import time
from datetime import datetime

import re #for regex queries
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
   return "Hello, World!. This is set of 3 APIs I made for your assignment"


class StdOutListener(StreamListener):
  def __init__(self, time_limit=60):
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
	        lang = datajson['lang']
	        tweet.insert_one({
		        "id": tid,
		        #uid as foreign key to reference to a user
		        "uid": uid,
		        "retweet_count": trtwtcount,
		        "fav_count": tfavcount,
		        "created_at": tcreate,
		        "text": ttext,
		        "mentions": tmention,
		        "lang": lang,
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
    # try:
	    print "Keyword passed is:-" 
	    print keyword
	    auth = OAuthHandler(consumer_key, consumer_secret)
	    auth.set_access_token(access_token, access_token_secret)

	    st = StdOutListener()
	    stream = Stream(auth, st)
	    stream.filter(track=[keyword])
	    print "First API done!"
	    response = {
			"status":"success",
		}
	    return jsonify(response)
	# except:
	#     response = {
	# 		"status":"failure",
	# 	}
	#     return jsonify(response)	

@app.route('/searchapi/',methods=['GET','POST'])

def search_data():
 #    name = request.args.get('name')
 #    print name
 #    response = {
 #        'success': "success",
 #    }
 #    return jsonify(response)
	# # except Exception as e
	# 	print (e)
	# return True

	# the type of search, like for name, rtcount etc.
	searchpara = request.args.get('sparam')

	#the possible values of the params
	name = request.args.get('name')
	sname = request.args.get('sname')
	favcount = request.args.get('favcount')
	rtcount = request.args.get('rtcount')
	sdate = request.args.get('start_date')
	edate = request.args.get('end_date')
	language = request.args.get('lang')
	ufollowc = request.args.get('ufollowcount')
	# umentions = request.args.get('user_mentions')
	ttxt = request.args.get('ttxt')	
	#operators are eq,lt,gt
	operator = request.args.get('operator')
	
	#string part sw,ew,cont,exact
	stringpart = request.args.get('stringpart')
	print searchpara
	sortdata = []
	if (searchpara=='name' or searchpara=='sname' or searchpara=='ttxt'):
		sortdata = string_search(name,sname,ttxt,stringpart)

	elif (searchpara=='rtcount' or searchpara=='favcount' or searchpara=='ufollowcount'):
		sortdata = int_search(rtcount,favcount,ufollowc,operator)

	# elif(searchpara=='data'):
	# 	sortdata = date_search(sdate,edate)

	elif(searchpara=='language'):
		usr = mongo.db.users
		twt = mongo.db.tweets
		curr = twt.find( {'lang':language})
		for i in curr:
			sortdata.append(i)

	return sortdata


def int_search(rtcount,favcount,ufollowc,operator):
	retans = []
	usr = mongo.db.users
	twt = mongo.db.tweets
	if (rtcount!=None):
		if (operator=='lt'):
			curr = twt.find( { 'retweet_count': {'$lt':rtcount}})
			for i in curr:
				retans.append(i)
			# retans.append(td)
		elif (operator=='lte'):
			curr = twt.find( { 'retweet_count': { '$lte': rtcount } })
			for i in curr:
				retans.append(i)
			# retans.append(td)
		if (operator=='gt'):
			curr = twt.find( { 'retweet_count': { '$gt': rtcount } })
			for i in curr:
				retans.append(i)
			# retans.append(td)
		if (operator=='gte'):
			curr = twt.find( { 'retweet_count': { '$gte': rtcount } })
			for i in curr:
				retans.append(i)
			# retans.append(td)
		if (operator=='eq'):
			curr = twt.find( { 'retweet_count': { '$eq': rtcount } })
			for i in curr:
				retans.append(i)
			# retans.append(td)

	elif (favcount!=None):
		if (operator=='lt'):
			curr = twt.find( { 'fav_count': { '$lt': favcount } })
			for i in curr:
				retans.append(i)
		elif (operator=='lte'):
			curr = twt.find( { 'fav_count': { '$lte': favcount } })
			for i in curr:
				retans.append(i)
		if (operator=='gt'):
			curr = twt.find( { 'fav_count': { '$gt': favcount } })
			for i in curr:
				retans.append(i)
		if (operator=='gte'):
			curr = twt.find( { 'fav_count': { '$gte': favcount } })
			for i in curr:
				retans.append(i)
		if (operator=='eq'):
			curr = twt.find( { 'fav_count': { '$eq': favcount } })
			for i in curr:
				retans.append(i)

	elif (ufollowc!=None):
		if (operator=='lt'):
			curr = twt.find( { 'fav_count': { '$lt': ufollowc } })
			for i in curr:
				retans.append(i)
		elif (operator=='lte'):
			curr = twt.find( { 'fav_count': { '$lte': ufollowc } })
			for i in curr:
				retans.append(i)
		if (operator=='gt'):
			curr = twt.find( { 'fav_count': { '$gt': ufollowc } })
			for i in curr:
				retans.append(i)
		if (operator=='gte'):
			curr = twt.find( { 'fav_count': { '$gte': ufollowc } })
			for i in curr:
				retans.append(i)
		if (operator=='eq'):
			td = twt.find( { 'fav_count': { '$eq': ufollowc } })
			for i in curr:
				retans.append(i)
	return (json_util.dumps(retans))


def string_search(name,sname,ttxt,stringpart):
	retans = []
	usr = mongo.db.users
	twt = mongo.db.tweets
	# return jsonify(usr.find())
	if (name!=None):
		if (stringpart=='exact'):
			ud = usr.find_one({'name': name})
			curr = twt.find( {'uid': ud['id']} )
			for i in curr:
				retans.append(i)
		# elif (stringpart=='sw'):
		# 	#({'files':{'$regex':'^File'}})
		# 	#regx = re.compile("^name", re.IGNORECASE)
		# 	regx = 
		# 	ud = usr.find_one({'name': regx })
		# 	td = twt.find( {'uid': ud['id']} )
		# 	retans.append(td)
		# elif (stringpart=='ew'):
		# 	ud = usr.find_one({'name': {'$regex':'^name'}})
		# 	td = twt.find( {'uid': ud['id']} )
		# 	retans.append(td)
	elif (sname!=None):
		ud = usr.find_one({'screen_name': sname})
		curr = twt.find( {'uid': ud['id']} )
		for i in curr:
			retans.append(i)		
	elif (ttxt!=None):
		curr = twt.find( {'uid': ud['id']} )
		for i in curr:
			retans.append(i)	
	# print "hola"
	return (json_util.dumps(retans))
# def date_search(sdate,edate):
# 	retans = []
# 	usr = mongo.db.users
# 	twt = mongo.db.tweets




# def search_function(name,sname,favcount,rtcount,sdate,edate,language,ufollowc,umentions,operator,stringpart):
# 	#we check for all the parameters passed, individually



@app.route('/makecsv/',methods=['GET','POST'])
def csvfile():
	searchpara = request.args.get('sparam')

	#the possible values of the params
	name = request.args.get('name')
	sname = request.args.get('sname')
	favcount = request.args.get('favcount')
	rtcount = request.args.get('rtcount')
	sdate = request.args.get('start_date')
	edate = request.args.get('end_date')
	language = request.args.get('lang')
	ufollowc = request.args.get('ufollowcount')
	# umentions = request.args.get('user_mentions')
	ttxt = request.args.get('ttxt')	
	#operators are eq,lt,gt
	operator = request.args.get('operator')
	
	#string part sw,ew,cont,exact
	stringpart = request.args.get('stringpart')
	print searchpara
	sortdata = []
	if (searchpara=='name' or searchpara=='sname' or searchpara=='ttxt'):
		sortdata = string_search(name,sname,ttxt,stringpart)

	elif (searchpara=='rtcount' or searchpara=='favcount' or searchpara=='ufollowcount'):
		sortdata = int_search(rtcount,favcount,ufollowc,operator)

	# elif(searchpara=='data'):
	# 	sortdata = date_search(sdate,edate)

	elif(searchpara=='language'):
		usr = mongo.db.users
		twt = mongo.db.tweets
		curr = twt.find( {'lang':language})
		for i in curr:
			sortdata.append(i)
	
	x = json.loads(sortdata)

	print "csvpart"
	f = csv.writer(open("out.csv", "wb+"))
	# f.writerow(["pk", "model", "codename", "name", "content_type"])
	for row in x:
		# f.writerow(row.values())
		f.writerow([row['id'],row['uid'],row['retweet_count'],row['fav_count'],row['created_at'],row['text'].encode("utf-8"),row['mentions'],row['lang']])
	print "csvpart2"
	response = {
		"status":"success, out.csv has the file",
	}
	return jsonify(response)
# 	flatdata = flattenjson(sortdata,',')

# 	flatdata = map( lambda x: flattenjson( x, "__" ), flatdata )

# 	columns = [ x for row in flatdata for x in row.keys() ]
# 	columns = list( set( columns ) )


# 	with open( fname, 'wb' ) as out_file:
# 	    csv_w = csv.writer( out_file )
# 	    csv_w.writerow( columns )

# 	    for i_r in flatdata:
# 	        csv_w.writerow( map( lambda x: i_r.get( x, "" ), columns ) )
# 	return True

# def flattenjson( b, delim ):
#     val = {}
#     for i in b.keys():
#         if isinstance( b[i], dict ):
#             get = flattenjson( b[i], delim )
#             for j in get.keys():
#                 val[ i + delim + j ] = get[j]
#         else:
#             val[i] = b[i]

#     return val


if __name__ == '__main__':
    app.run(debug=True)