В сессиях использовался AES CBC, и, если поломать сессию, вылетала ошибка паддинга, что
позволяет провести атаку [padding oracle](https://habr.com/ru/post/247527/) (смотрите [сплоит](sploit/sploit.py)).