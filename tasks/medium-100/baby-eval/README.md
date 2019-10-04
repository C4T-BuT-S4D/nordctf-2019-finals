# Medium-100 | Web | Baby Eval

## Информация

> Как известно, в PHP даже любой NOTICE может привести к RCE. Если не верите, попробуйте убедиться в этом сами.
> 
> http://address:33034


## Запуск

```sh
docker-compose up --build -d
```


## Описание

Единственное, что делает сервис, это вызывает [eval()](https://www.php.net/manual/ru/function.eval.php) от пользовательского ввода. Есть подсказка, что флаг лежит в файле `/tmp/flag.txt`. 

После вызова `phpinfo();` можно заметить некоторые ограничения:

- функции, позволяющие исполнить команды шелла, запрещены через директиву [disable_functions](https://www.php.net/manual/ru/ini.core.php#ini.disable-functions)
- файлы, к которым PHP имеет доступ, [ограничены](https://www.php.net/manual/ru/ini.core.php#ini.open-basedir) директорией `/var/www/html/`


## Решение

При просмотре страницы `phpinfo();` в глаза бросается директива `imap.enable_insecure_rsh = On`. Это наводит на [баг в PHP](https://bugs.php.net/bug.php?id=76428), который может привести к исполнению произвольного кода через функцию [imap_open](https://www.php.net/manual/ru/function.imap-open.php).

Мы не можем видеть результат выполнения команды напрямую, поэтому можно использовать внешние сервисы (или поднимать свои) и подключаться к ним через nc/wget/curl. Также в ограниченной среде не работает разрешение доменных имён, нужно использовать IP-адреса при подключении.

[Пример эксплоита](exploit.php)


## Флаг

Флаг лежит в файле [service/flag.txt](service/flag.txt).

`flag{some_notice_based_rce_for_you}`
