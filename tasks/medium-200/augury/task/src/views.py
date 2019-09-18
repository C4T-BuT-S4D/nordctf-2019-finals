from flask import render_template, url_for, redirect, flash

from app import app, FLAG
from helpers import *


@app.route("/")
def main():
    username = decode_cookies()
    return render_template('index.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username is None or password is None:
            flash('You need to enter username and password')
            return redirect(url_for('login'))

        with database() as (curs, _):
            query = 'SELECT id FROM users WHERE username = ? AND password = ?'
            curs.execute(query, (username, password))
            user = curs.fetchone()

        if not user:
            flash('Invalid credentials')
            return redirect(url_for('login'))

        resp = make_response(redirect(url_for('main')))

        cookie = {'username': username, 'key': AES_KEY}
        cookie_data = json.dumps(cookie)
        encrypted = AESCipher(AES_KEY).encrypt(cookie_data)
        resp.set_cookie('cookie', encrypted)

        flash(f'You successfully logged in as {username}!')

        return resp
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username is None or password is None:
            flash('You need to enter username and password')
            return redirect(url_for('register'))

        if username == 'admin':
            flash('Can\'t register admin user')
            return redirect(url_for('register'))

        with database() as (curs, _):
            query = 'SELECT id FROM users WHERE username = ?'
            curs.execute(query, (username,))
            user = curs.fetchone()

        if user:
            flash('Username taken')
            return redirect(url_for('register'))

        with database() as (curs, conn):
            query = 'INSERT INTO users (username, password) VALUES (?, ?)'
            curs.execute(query, (username, password))
            conn.commit()

        return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route('/logout')
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie('cookie', '', expires=0)
    flash('Logout successful!')
    return resp


@app.route('/admin', methods=['GET'])
def admin_page():
    username = decode_cookies(raise_exception=True)
    if username != 'admin':
        return redirect(url_for('main'))
    return render_template('admin.html', flag=FLAG)
