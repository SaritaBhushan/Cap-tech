FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /UserJWTAuth
WORKDIR /UserJWTAuth

ENV USER=root

COPY requirements.txt /UserJWTAuth/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ADD . /UserJWTAuth/