# Hard-400 | Pwn | wee

## Информация

> Смотри какой маленький бинарник у нас получилось собрать!
> 
> `nc address 33074`


## Запуск

```sh
cd deploy
./make_docker.sh
./worker.sh
```


## Описание

Дан бинарник в котором всего 3 функции. Функция main читает буфер и перезаписывает адрес возврата.


## Решение
Внутри бинарника есть функция, которая делает sigret syscall, с помощью неё можно осуществить атаку SROP.


[Пример эксплоита](solve/exploit.py)


## Флаг

`flag{6a1a778143e4672886991729035807cabeb75ad42a3fe4bf580cfbdf5cea7c476705d878af5f0fd0dc07d19f2959e224b21788e561f046177f6752b4bcc59e2c}`
