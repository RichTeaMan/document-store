from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import couchdb
from json import dumps
from datetime import datetime

app = Flask(__name__)
api = Api(app)
couch = couchdb.Server()
couch.resource.credentials = ("admin", "password")
db = couch['document']

class Scan(Resource):    
    def put(self):
        print('Document store requested.')
        document = request.files['document'].read()
        key = request.headers.get('key')
        print (document)
        row = { 'document': document, 'timestamp': datetime.now().isoformat() }
        if key:
            row['_id'] = key
        try:
            savedKey = db.save(row)
            return savedKey['_id'], 200
        except couchdb.http.ResourceConflict as e:
            print(e)
            return 'key conflict', 409

    def get(self):
        print('Document retrieve requested.')
        key = request.args.get('key')
        if not key:
            return 'A key query parameter must be specified', 400
        row = db.get(key)
        if row:
            return row['document'], 200
        else:
            return f"Document with key '{key}' not found.", 404

api.add_resource(Scan, '/document') # Route_1

if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5002')
