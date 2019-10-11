FROM ubuntu:latest

RUN apt-get update

ADD --chown=root ./app/kernelstorage /kernelstorage
ADD --chown=root ./app/debug /debug

WORKDIR /

ENTRYPOINT /kernelstorage