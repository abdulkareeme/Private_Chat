FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y python3-dev libpq-dev build-essential

WORKDIR /usr/src/chat_app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFRED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/chat_app/requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/chat_app/entrypoint.sh

COPY . /usr/src/chat_app/

ENTRYPOINT [ "/usr/src/chat_app/entrypoint.sh" ]