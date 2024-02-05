FROM python:3

WORKDIR /homework_272

COPY ./requirements.txt /homework_272/

RUN pip install -r /homework_272/requirements.txt

COPY . .