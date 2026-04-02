FROM python:3.8-slim-buster
WORKDIR /usr/src
COPY ./requirements.txt /usr/src
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download de_core_news_md
COPY ./src /usr/src
COPY ./data/model /usr/data/model


EXPOSE 4545
#CMD ["gunicorn","wsgi:app", "--timeout", "9000","--bind", "0.0.0.0:4545"]
CMD [ "python","-u", "app.py" ]
