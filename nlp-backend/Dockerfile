FROM python:3.8-slim-buster
WORKDIR /usr/src
COPY ./requirements.txt /usr/src
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download de_core_news_lg
COPY ./src /usr/src
COPY ./data /usr/data
COPY ./log /usr/log
EXPOSE 8070
#CMD ["gunicorn","wsgi:app", "--timeout", "9000","--bind", "0.0.0.0:8070"]
CMD [ "python","-u", "app.py" ]
