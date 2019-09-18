from flask import Flask

from helpers import *

config = json.load(open('config.json', 'r'))

app = Flask(__name__)
app.secret_key = config['SECRET_KEY']
FLAG = config['FLAG']

from views import *


@app.before_first_request
def init_db():
    with database() as (curs, conn):
        query = '''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(255),
            password VARCHAR(255)
        )'''
        curs.execute(query)


if __name__ == "__main__":
    app.run(debug=True)
