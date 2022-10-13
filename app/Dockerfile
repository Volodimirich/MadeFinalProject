FROM python:3.9-alpine

RUN mkdir -p /usr/src/app
COPY ./requirements.txt /usr/src/app
RUN cd /usr/src/app && python -m pip install -r requirements.txt

WORKDIR /usr/src/app
EXPOSE 8000
