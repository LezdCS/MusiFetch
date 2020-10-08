FROM python
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install \
    ffmpeg \
    postgresql postgresql-contrib -y

ADD requirements.txt /
RUN pip install -r code/requirements.txt