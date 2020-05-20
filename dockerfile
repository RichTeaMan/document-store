FROM python:3.8.3-buster

WORKDIR /document-store
ADD requirements.txt /document-store/
RUN pip install -r requirements.txt

ADD *.py /document-store/

ENTRYPOINT python server.py
