FROM python:3.8
RUN mkdir /code
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

ADD  ./requirements.txt /code/
RUN  /usr/local/bin/python -m pip install --upgrade pip; pip install -r /code/requirements.txt
ADD . /code/
