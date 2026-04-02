FROM python:3

ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD *.py ./

ENV BROKER_ADDRESS=mosquitto
ENV PORT=1883
ENV KEEPALIVE=60
ENV NO_DATA_MESSAGE=topic/entityNotFound
ENV ANSWER_MESSAGE=topic/suggestAnswer
ENV API_ENDPOINT_WIKIDATA=https://www.wikidata.org/w/api.php

ENTRYPOINT [ "python", "-u", "mqtt_subscriber.py" ]
