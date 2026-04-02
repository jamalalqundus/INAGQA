FROM python:3
WORKDIR /tests
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py .

RUN chown 1001:0 -R /tests && \
chmod g=u -R /tests

USER 1001
CMD ["pytest"]