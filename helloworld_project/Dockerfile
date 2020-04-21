FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /helloworld_project
WORKDIR /helloworld_project
ADD requirements.txt /helloworld_project/

RUN pip install -U pip
RUN pip install -r requirements.txt

ADD . /helloworld_project/
EXPOSE 80
