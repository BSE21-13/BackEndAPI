import os
from flask import Flask, json
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin


load_dotenv() 

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = 'secret_key'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo  = PyMongo(app)

@app.route('/search', methods=['GET'])
@cross_origin()
def query_resource():
    queryString = request.args.get('q')
    results = {
        "keywords":[queryString, "law", "state", "prosecution", "police", "unfair", "appeal"], 
        
    "results" : [{
        
        "chapter":"Chapter 1",
        "text":" The  people  shall  express  their  will  and  consent  on  who  shall govern them and how\nthey should be governed, through regular, free and fair elections of their representatives or through referenda.",
    },
    {
        "chapter":"Chapter 13",
        "text":" The  people  shall  express  their  will  and  consent  on  who  shall govern them and how\nthey should be governed, through regular, free and fair elections of their representatives or through referenda.",
    },
    {
        "chapter":"Chapter 11",
        "text":" The  people  shall  express  their  will  and  consent  on  who  shall govern them and how\nthey should be governed, through regular, free and fair elections of their representatives or through referenda.",
    },
    {
        "chapter":"Chapter 8",
        "text":" The  people  shall  express  their  will  and  consent  on  who  shall govern them and how\nthey should be governed, through regular, free and fair elections of their representatives or through referenda.",
    },
    {
        "chapter":"Chapter 5",
        "text":" The  people  shall  express  their  will  and  consent  on  who  shall govern them and how\nthey should be governed, through regular, free and fair elections of their representatives or through referenda.",
    }
    ]}

    resp = jsonify(results)
    resp.status_code = 200
    return resp


@app.errorhandler(404)
@cross_origin()
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }

    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ :
    app.run(debug=True)


