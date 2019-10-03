import json

import requests
from flask import Flask, render_template, request, flash, redirect, url_for

config = json.load(open('config.json', 'r'))

app = Flask(__name__)
app.secret_key = config['SECRET_KEY']
FLAG = config['FLAG']
URL = 'http://pomo-mondreganto.me/request_bin/bin/93ede9ef65?q={part}'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/leak', methods=['POST'])
def process():
    username = request.form.get('username')
    password = request.form.get('password')
    host = request.form.get('host')
    port = request.form.get('port')

    if not (username and password and host and port):
        flash("Invalid data")
        return redirect(url_for('index'))

    proxy_url = f'socks5://{username}:{password}@{host}:{port}'
    proxies = {
        'http': proxy_url,
        'https': proxy_url,
    }

    for i in range(0, len(FLAG), 10):
        part = FLAG[i:i + 10]
        url = URL.format(part=part)
        try:
            r = requests.get(url, proxies=proxies)
        except Exception as e:
            print(e)
            pass

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
