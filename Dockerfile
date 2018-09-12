FROM python:3.7

MAINTAINER      lecon "leconio@outlook.com"

RUN mkdir /www

ADD ./server/ /www/

WORKDIR /www

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3","punch_server.py"]