from flask import Flask, json
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key"
app.config["MONGO_URI"] = "mongodb+srv://michaelaries:6gf3WE8kRkpUGeh@cluster0.j1cpf.mongodb.net/CADISE?retryWrites=true&w=majority"
mongo  = PyMongo(app)


@app.route('/search', methods=['GET'])
def query_resource():
   resp = jsonify('Resource Queried, Results sent succesffuly.')
   resp.status_code = 200
   return resp


@app.errorhandler(404)
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


