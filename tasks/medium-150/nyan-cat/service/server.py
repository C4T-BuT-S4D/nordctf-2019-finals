#!/usr/bin/env python3

from flask import Flask, request, make_response, redirect, render_template, url_for
from sessions import make_session_cookie, read_session_cookie


app = Flask(__name__, static_folder='static')

with open('flag.txt', 'r') as file:
    FLAG = file.read()


def get_nyan_info(broken):
    if broken:
        return url_for('static', filename='broken.gif'), 'My Nyan Cat is still broken :('
    return url_for('static', filename='fixed.gif'), FLAG


@app.route('/init')
def init():
    session = {'broken': True}
    response = make_response(redirect(url_for('main')))
    response.set_cookie('session', make_session_cookie(session))
    return response


@app.route('/')
def main():
    if 'session' in request.cookies:
        session = read_session_cookie(request.cookies.get('session'))
        if session is not None and 'broken' in session:
            broken = session.get('broken')
            image, message = get_nyan_info(broken)
            return render_template('index.html', image=image, message=message)
    response = make_response(redirect(url_for('init')))
    response.set_cookie('session', '', expires=0)
    return response


if __name__ == '__main__':
    app.run('0.0.0.0', port=31337, threaded=True)
