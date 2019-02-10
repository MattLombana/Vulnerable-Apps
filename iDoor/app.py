#! /usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import database as db


DEBUG = False
SESSION_COOKIE_HTTPONLY = False

app = Flask(__name__)
app.secret_key = 'SUPERSECRETKEY'
app.config['SESSION_COOKIE_HTTPONLY'] = False
login_manager = LoginManager()
login_manager.session_protection = None
login_manager.init_app(app)


@app.route('/index')
@app.route('/')
def index():
    args = {'active': 'index'}
    return render_template('index.html', args=args)


@app.route('/about')
def about():
    args = {'active': 'about'}
    return render_template('about.html', args=args)


@app.route('/doors/<doorid>')
def doors(doorid):
    args = {'active': 'doors', 'doorid': doorid}
    return render_template('doors.html', args=args)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.user_exists(username):
            flash('The Username {} is Already Taken'.format(username))
            return redirect(url_for('register'))
        else:
            db.insert_user(username, password)
            return redirect(url_for('login'))
    else:
        args = {'active': 'register'}
        return render_template('register.html', args=args)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not db.user_exists(username):
            flash("Username Doesn't Exist, Make Sure To Register")
            return redirect(url_for('register'))

        user_password = db.get_user_password(username)

        if password == user_password:
            db.mark_loggedin(username)
            user = db.get_user_by_username(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Username and Password Combination is Incorrect')
            return redirect(url_for('login'))
    else:
        args = {'active': 'login'}
        return render_template('login.html', args=args)


@app.route('/logout')
@login_required
def logout():
    db.mark_loggedout(current_user.username)
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
        return db.get_user_by_id(user_id)


if __name__ == '__main__':
    db.initialize_db()
    app.run(host='0.0.0.0', debug=DEBUG)
