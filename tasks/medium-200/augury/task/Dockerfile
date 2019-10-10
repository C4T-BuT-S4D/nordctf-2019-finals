FROM python:3.7-alpine

MAINTAINER @pomo_mondreganto

ENV PYTHONUNBUFFERED=1

RUN apk add gcc musl-dev

RUN pip install gunicorn gevent

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD src /app
WORKDIR /app

CMD ["gunicorn", "--worker-class", "gevent", "-b", "0.0.0.0", "--worker-connections", "1024", "app:app"]