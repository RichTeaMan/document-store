import os
import requests
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
import couchdb
from json import dumps
from datetime import datetime

app = Flask(__name__)
api = Api(app)

databaseName = 'document-store'

couchdb_address = os.getenv('DB_ADDRESS')
if not couchdb_address:
    couchdb_address = 'http://localhost:5984'

couchdb_username = os.getenv('DB_USERNAME')
if not couchdb_username:
    couchdb_username = 'admin'

couchdb_password = os.getenv('DB_PASSWORD')
if not couchdb_password:
    couchdb_password = 'password'

print('Set environment variable DB_ADDRESS to change connection URL.')
print(f'Establishing database connection at {couchdb_address}...')

couchServer = couchdb.Server(couchdb_address)
couchServer.resource.credentials = (couchdb_username, couchdb_password)
if databaseName in couchServer:
    db = couchServer[databaseName]
else:
    db = couchServer.create(databaseName)

print('Database found.')

def saveDocument(key: str, document: str, headers):

    row = {
        'document': document ,
        'timestamp': datetime.now().isoformat(),
        'headers': headers
    }
    if key:
        row['_id'] = key
    savedRow = db.save(row)
    savedKey = savedRow[0]
    return savedKey

class Home(Resource):
    def get(self):
        return 'Document store', 200

class Store(Resource):
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
        try:
            savedKey = saveDocument(key, document, {})
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
        if not row:
            # page not found, go get it
            response = requests.get(key)
            if response.ok:
                headerDict = {}
                for h in response.headers:
                    value = response.headers.get(h)
                    headerDict[h] = value
                try:
                    saveDocument(key, response.text, headerDict)
                except couchdb.http.ResourceConflict as e:
                    # do nothing, just relaod from DB as normal
                    print(e)
                row = db.get(key)
            else:
                print(f"Error retrieving document '{key}', code {response.status_code}.")
                return f"Error retrieving document '{key}'", response.status_code

        if row:
            contentType = row['headers'].get('Content-Type')
            contentLength = row['headers'].get('Content-Length')
            resp = make_response(row['document'], 200)
            if contentType:
                resp.headers['Content-Type'] = contentType
            if contentLength:
                resp.headers['Content-Length'] = contentLength
            return resp
        else:
            return f"Document with key '{key}' not found.", 404

api.add_resource(Home, '/')
api.add_resource(Store, '/document')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5002')
