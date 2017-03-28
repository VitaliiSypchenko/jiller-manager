# use base python image with python 2.7
FROM python:latest

# add requirements.txt to the image

# set working directory to /app/
WORKDIR /app/
ADD . /app
# install python dependencies
RUN pip install -r requirements.txt

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser
