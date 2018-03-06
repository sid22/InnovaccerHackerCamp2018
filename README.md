# Twitter Stream/Store/Search


**For Innoavacer assignment**
  - Uses Twitter stream for AP1
  - Search funtionality as API2
  - Export to CSV as API3
  - Uses NoSQL db, MongoDB
  
# Stream API

This API triggers storage of a stream of tweets for the given keyword for one minute. The time limit can be varied easily. To keep the API result consistent, however I have decided to hard code it.

API ``` 127.0.0.1:5000/streamapi/<string:keyword>'```
Method supported: POST

Example
> 127.0.0.1:5000/streamapi/emmawatson

The API response for a succefull run is
> {
>    "status": "success"
>}

# Search API

This API is to query the stored data and display the relevant results.

API ``` 127.0.0.1:5000/searchapi/{{the query}}'```
Method supported: POST, GET

The query can be made for a variety of parameters both string based and numerical based.

| Key | Possible Values | Description | 
| ------ | ------ | ------ |
| searchparam | any other key, ex: name | this key is to specify which key based query is to be made | 
| name | string | to specify name to be searched
| sname | string | to specify screen name to be searched
| favcount | int type | to specify fav count
| rtcount | int type | to specify retweet count
| language | string but fixed, en, fr etc | to specify language
| ufollowc | int type | number of followers of user who made tweet | 
| ttxt | string | to search by tweet text |

Special keys
| Key | Possible Values | Description | 
| ------ | ------ | ------ |
| operator | eq,lt,lte,gt,gte | to give relation to given int values
| stringpart | exact | specifying the text as exact

Example
> 127.0.0.1:5000/searchapi/?sparam=name&name=Doc Willis&stringpart=exact
>
> 127.0.0.1:5000/searchapi/?sparam=rtcount&rtcount=6&operator=lt

The API response for a succefull run is
> The json data obtained

# CSV API

API ``` 127.0.0.1:5000/makecsv/{{the query}}'```
Method supported: POST, GET

The {{query }} part is similar to search API,the results are stored in out.csv file, locally in the folder itself.

### Installation

```sh
$ git clone https://github.com/goyal-sidd/twitter-stream.git
$ cd twitter-stream
$ virtualenv venv (Optional step)
$ source venv/bin/activate (optional, cont.)
$ pip install -r requirements.txt
$ python app.py
```

### Technologies used

 - Flask
 - MongoDB

-Siddarth Goyal

