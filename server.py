from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import couchdb
from json import dumps
from datetime import datetime

app = Flask(__name__)
api = Api(app)

databaseName = 'document'

couchServer = couchdb.Server('http://192.168.1.228:5984')
couchServer.resource.credentials = ("admin", "password")
if databaseName in couchServer:
    db = couchServer[databaseName]
else:
    db = couchServer.create(databaseName)

class Scan(Resource):    
    def put(self):
        print('Document store requested.')

        # attempt different data fetch depending on headers
        document = request.get_data()
        # content_type: application/x-www-form-urlencoded
        if not document:
            document = list(request.form.keys())[0]
        if not document:
            return 'Document is empty', 400
        key = request.headers.get('key')
        row = {
            'document': document ,
            'timestamp': datetime.now().isoformat()
            }
        if key:
            row['_id'] = key
        try:
            savedRow = db.save(row)
            savedKey = savedRow[0]
            return { 'key': savedKey }, 200
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
