FROM ubuntu:latest
RUN apt-get update && apt-get install -y socat
RUN mkdir /home/task
WORKDIR /home/task/
ADD crackk flag.txt ./
RUN chmod +x ./crackk
ENTRYPOINT ["socat", "TCP-LISTEN:34567,reuseaddr,fork", "EXEC:./crackk"]