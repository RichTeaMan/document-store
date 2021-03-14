FROM python:3.8.3-buster

LABEL org.opencontainers.image.source https://github.com/richteaman/document-store

WORKDIR /document-store
ADD requirements.txt /document-store/
RUN pip install -r requirements.txt

ADD *.py /document-store/

ENTRYPOINT python server.py
