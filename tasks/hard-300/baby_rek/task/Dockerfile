FROM python:3.7-alpine

RUN apk add socat gcc musl-dev

RUN pip install pycrypto

RUN mkdir /app

WORKDIR /app

ADD main.py .
ADD flag.txt .

RUN chmod +x main.py

ENTRYPOINT ["socat", "TCP-LISTEN:31337,fork,reuseaddr", "EXEC:./main.py,pty"]