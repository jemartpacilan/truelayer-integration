FROM python:3.8.2-alpine

WORKDIR /usr/src

ENV FLASK_APP=app/routes.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apk update
RUN apk add --no-cache python3-dev gcc musl-dev linux-headers libffi-dev openssl-dev libressl-dev

COPY Pipfile Pipfile.lock ./


RUN pip install --upgrade setuptools pip
RUN pip install pipenv && pipenv install --sequential --system --deploy

RUN pip install python-dotenv

EXPOSE 5000

COPY . .

CMD flask run