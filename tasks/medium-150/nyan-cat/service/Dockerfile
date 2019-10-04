FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN useradd -s /bin/false -m task

WORKDIR /home/task/

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD flag.txt server.py sessions.py gunicorn.conf.py ./
ADD static ./static
ADD templates ./templates

ENTRYPOINT ["gunicorn", "--config", "gunicorn.conf.py", "server:app"]
