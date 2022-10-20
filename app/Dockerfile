FROM python:3.8-slim as base

RUN python -m pip install -U pip && python -m pip install --upgrade setuptools && mkdir -p /usr/src/app
COPY ./requirements.txt /usr/src/app
# RUN apt update && apt install build-essential -y
RUN cd /usr/src/app && python -m pip install -r requirements.txt
# RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

WORKDIR /usr/src/app
EXPOSE 8000
