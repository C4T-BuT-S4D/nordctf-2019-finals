FROM ubuntu:latest

RUN apt-get update

ADD --chown=root ./app/tester /tester
ADD --chown=root ./app/flag.txt /flag.txt

WORKDIR /

ENTRYPOINT /tester
