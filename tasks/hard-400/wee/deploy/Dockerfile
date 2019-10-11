FROM ubuntu:latest

RUN apt-get update

ADD --chown=root ./app/wee /wee
ADD --chown=root ./app/flag /flag

WORKDIR /

ENTRYPOINT /wee
