FROM keltecc/nsjail:latest

RUN apt update && \
    apt install -y ssh \
                   wget curl netcat \
                   php-fpm php-imap 

RUN mkdir /chroot/
WORKDIR /chroot/

RUN mkdir -p ./usr/lib/php/ && \
    cp -R /lib* . && \
    cp -R /usr/lib* ./usr/ && \
    cp -R /usr/lib/php/* ./usr/lib/php/

RUN mkdir ./dev && \
    mknod ./dev/null c 1 3 && \
    mknod ./dev/zero c 1 5 && \
    mknod ./dev/random c 1 8 && \
    mknod ./dev/urandom c 1 9 && \
    chmod 666 ./dev/*

RUN mkdir -p ./bin/ && \
    cp /bin/sh \
       /bin/ls \
       /bin/nc \
       /bin/cat \
       /bin/pwd \
       ./bin/ && \
    ln -s /bin/sh ./bin/bash && \
    chmod 111 ./bin/*

RUN mkdir -p ./usr/bin/ && \
    cp /usr/bin/id \
       /usr/bin/rsh \
       /usr/bin/curl \
       /usr/bin/wget \
       /usr/bin/base64 \
       /usr/bin/whoami \
       ./usr/bin/ && \
    chmod 111 ./usr/bin/*

RUN mkdir -p ./usr/sbin/ && \
    cp /usr/sbin/php-fpm* ./usr/sbin/php-fpm && \
    chmod 111 ./usr/sbin/*

RUN mkdir ./etc/ && \
    cp /etc/passwd ./etc/ && \
    chmod 444 ./etc/*

RUN mkdir ./tmp/ && \
    chmod 777 ./tmp/ && \
    chmod +t ./tmp/

RUN mkdir -p ./var/www/html/

ADD flag.txt ./tmp/
ADD index.php ./var/www/html/
ADD php/php.ini php/php-fpm.conf ./etc/

RUN chmod 444 ./tmp/flag.txt \
              ./var/www/html/index.php \
              ./etc/php.ini \
              ./etc/php-fpm.conf

WORKDIR /

ADD nsjail/nsjail.sh /nsjail.sh
RUN chmod 555 /nsjail.sh

ENTRYPOINT ["/nsjail.sh"]
CMD ["/usr/sbin/php-fpm", "-F", "-O", "-y", "/etc/php-fpm.conf", "-c", "/etc/php.ini"]
