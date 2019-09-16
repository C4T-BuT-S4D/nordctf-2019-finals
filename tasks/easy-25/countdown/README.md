# Easy-25 | Web | Countdown

## Информация

> И узрит Его всякое око. И силые небесные поколеблются. И восплачутся все племена земные. Ибо увидят Его, грядущего с силою и славою великою.
>
> Так древние люди описывали приход 31337 года. Чтобы не пропустить это событие, мы запустили таймер с обратным отсчётом. Действительно ли 31337 год настолько далеко?
> 
> http://address:33014


## Запуск

```sh
docker-compose up --build -d
```


## Описание

На сайте крутится таймер с обратным отсчётом до 31337 года. Нет никакого пользовательского ввода, стили и скрипты подгружаются из директории `/static/`.


## Решение

Если посмотреть в заголовки ответа сервера, можно увидеть кастомный заголовок:

```
X-Hint: Robots will live!
```

Это подсказка посмотреть в файл [robots.txt](https://ru.wikipedia.org/wiki/Стандарт_исключений_для_роботов). Переходим на него и видим ссылку на флаг, который прячется в директории со статикой:

```
User-Agent: *

Disallow: /static/flag_807d0fbcae7c4b20518d4d85664f6820aafdf936104122c5073e7744c46c4b87.txt
```

[Пример эксплоита](exploit.sh)


## Флаг

Флаг лежит в файле [service/static/flag_807d0fbcae7c4b20518d4d85664f6820aafdf936104122c5073e7744c46c4b87.txt](service/static/flag_807d0fbcae7c4b20518d4d85664f6820aafdf936104122c5073e7744c46c4b87.txt).

`flag{31337_is_coming_please_wait}`