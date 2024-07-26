FROM python:3.12

RUN mkdir /advertisement_api

WORKDIR /advertisement_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

ENV PYTHONPATH=/advertisement_api/src
