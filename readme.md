# Document Store

A project for storing document in [Apache CouchDB](https://couchdb.apache.org/).

## Installing and Running

Installing:
```
pip install virtualenv
virtualenv venv
pip install -r requirements.txt
```

Running:
```
python server.py
```

## Usage

### Document Store

```bash
curl -X PUT http://localhost:5002/document --data "document=@filepath_to_store" -H 'key: document_key' -v
```

### Document Retrieval

```bash
curl -X GET http://localhost:5002/document?key=document_key
```

If the given document does not exist in the database it will be fetched, saved, then returned.

The response will have the original content-type and content-length headers.

## Docker

Create image:
```
sudo docker build -t document-store .
```

Run container:
```
sudo docker run -d -p 5002:5002 --name document-store document-store
```

## API Reference

A Swagger reference is available in swagger.yml.
