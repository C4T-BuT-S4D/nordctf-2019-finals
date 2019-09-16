FROM python:2.7-alpine

RUN apk update && \
    apk add socat

RUN adduser -s /bin/false -D task

WORKDIR /home/task/

ADD requirements.txt ./

RUN pip install -r requirements.txt

ADD task.py flag.txt ./

RUN chmod 555 task.py && \
    chmod 444 flag.txt

ENTRYPOINT ["socat", "TCP-LISTEN:31337,reuseaddr,fork", "EXEC:'timeout 5 ./task.py',su=task"]
