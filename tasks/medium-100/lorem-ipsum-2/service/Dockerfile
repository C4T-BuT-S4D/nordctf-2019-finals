FROM python:2.7

RUN apt update && \
    apt install -y socat stegsnow

RUN useradd -s /bin/false -m task

WORKDIR /home/task/

ADD requirements.txt ./

RUN pip install -r requirements.txt

ADD task.py flag.txt ./

RUN chmod 555 task.py && \
    chmod 444 flag.txt

ENTRYPOINT ["socat", "TCP-LISTEN:31337,reuseaddr,fork", "EXEC:./task.py,su=task"]
