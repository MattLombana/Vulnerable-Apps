import sqlite3 as sql
from user import User


DATABASE = './data/database.db'


def initialize_db():
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("drop table if exists users")
    cur.execute("drop table if exists posts")
    cur.execute("drop table if exists adminmessages")
    cur.execute("create table users (id integer primary key autoincrement, username text not null, password text not null, authenticated integer not null, admin integer not null)")
    cur.execute("create table posts (id integer primary key autoincrement, author text not null, message text not null)")
    cur.execute("create table adminmessages (id integer primary key autoincrement, message text not null)")
    cur.execute("INSERT INTO users (username,password,authenticated,admin) VALUES ('admin', 'secret', 0, 1)")
    cur.execute("INSERT INTO users (username,password,authenticated,admin) VALUES ('foo', 'bar', 0, 0)")
    cur.execute("INSERT INTO posts (author,message) VALUES ('Matt', 'Before I run, I like something sweet, like cookies!')")
    cur.execute("INSERT INTO posts (author,message) VALUES ('Matt', 'After I run, I like something savory, like BeEF!')")
    cur.execute("INSERT INTO adminmessages (message) VALUES ('Test')")
    cur.execute("INSERT INTO adminmessages (message) VALUES ('Test2')")
    con.commit()
    con.close()


def insert_user(username, password):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password,authenticated, admin) VALUES ('{}', '{}', 0, 0)".format(username, password))
    con.commit()
    con.close()


def get_user_by_id(user_id):
    if type(user_id) != int:
        return None
    con = sql.connect(DATABASE)
    cur = con.cursor()
    results = cur.execute("SELECT * FROM users WHERE id = {}".format(user_id))
    res = results.fetchone()
    con.close()
    if res:
        user = User(res[0], res[1], bool(res[3]), bool(res[4]))
        return user
    else:
        return None


def get_user_by_username(username):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    results = cur.execute("SELECT * FROM users WHERE username = '{}'".format(username))
    res = results.fetchone()
    con.close()
    if res:
        user = User(res[0], res[1], bool(res[3]), bool(res[4]))
        return user
    else:
        return None


def user_exists(username):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    results = cur.execute("SELECT * FROM users WHERE username = '{}'".format(username))
    res = results.fetchone()
    con.close()
    return bool(res)


def get_user_password(username):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    results = cur.execute("SELECT * FROM users WHERE username = '{}'".format(username))
    res = results.fetchone()
    con.close()
    if res:
        return res[2]
    return ''


def mark_loggedin(username):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("UPDATE users SET authenticated = 1 WHERE username = '{}'".format(username))
    con.commit()
    con.close()


def mark_loggedout(username):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("UPDATE users SET authenticated = 0 WHERE username = '{}'".format(username))
    con.commit()
    con.close()


def mark_admin(username):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("UPDATE users SET admin = 1 WHERE username = '{}'".format(username))
    con.commit()
    con.close()


def insert_post(author, message):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO posts (author,message) VALUES ('{}', '{}')".format(author, message))
    con.commit()
    con.close()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_posts():
    con = sql.connect(DATABASE)
    con.row_factory = dict_factory
    cur = con.cursor()
    results = cur.execute("SELECT * FROM posts").fetchall()
    con.close()
    return results


def insert_admin_message(message):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO adminmessages (message) VALUES ('{}')".format(message))
    con.commit()
    con.close()


def get_admin_messages():
    con = sql.connect(DATABASE)
    con.row_factory = lambda cursor, row: row[1]
    cur = con.cursor()
    results = cur.execute("SELECT * FROM adminmessages").fetchall()
    con.close()
    return results
