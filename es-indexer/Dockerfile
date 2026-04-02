FROM python:3.6.10-alpine

WORKDIR /app

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

#run non-priviledged
RUN adduser --gecos "" --disabled-password worker
USER worker

COPY data /app/data
COPY addIndex.py /app/addIndex.py

ENV ELASTICSEARCH_URL = 'http://elasticsearch:9200'

ENTRYPOINT [ "python","-u" ]
CMD [ "addIndex.py" ]

