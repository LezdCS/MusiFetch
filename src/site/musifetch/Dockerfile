FROM python:3.7
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install \
    ffmpeg \
    postgresql postgresql-contrib -y

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code/