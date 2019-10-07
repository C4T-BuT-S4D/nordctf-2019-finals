FROM ubuntu:18.04

RUN apt update && \
    apt install -y php-fpm

RUN useradd -s /bin/false -m task

RUN mkdir -p /var/www/html/

WORKDIR /var/www/html/

ADD php/php.ini php/php-fpm.conf /etc/

ADD index.php dump.html ./

RUN mv /usr/sbin/php-fpm* /usr/sbin/php-fpm 

ENTRYPOINT ["php-fpm", "-F", "-O", "-y", "/etc/php-fpm.conf", "-c", "/etc/php.ini"]
