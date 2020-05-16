FROM python

ADD *.py /document-store/
ADD requirements.txt /document-store/

WORKDIR /document-store
RUN pip install -r requirements.txt

ENTRYPOINT python server.py
