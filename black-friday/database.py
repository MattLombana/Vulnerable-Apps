import sqlite3 as sql
from user import User


DATABASE = './data/database.db'


def initialize_db():
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("drop table if exists users")
    cur.execute("drop table if exists products")
    cur.execute("drop table if exists orders")
    cur.execute("create table users (id integer primary key autoincrement, username text not null, password text not null, authenticated integer not null, admin integer not null)")
    cur.execute("create table products (id integer primary key autoincrement, name text not null, price integer not null)")
    cur.execute("create table orders (id integer primary key autoincrement, date text not null, cost integer not null, items text not null, user_id integer not null, FOREIGN KEY(user_id) REFERENCES users(id))")
    cur.execute("INSERT INTO users (username,password,authenticated,admin) VALUES ('admin', 'secret', 0, 1)")
    cur.execute("INSERT INTO users (username,password,authenticated,admin) VALUES ('foo', 'bar', 0, 0)")
    cur.execute("INSERT INTO products (name, price) VALUES ('tv', 1337)")
    cur.execute("INSERT INTO products (name, price) VALUES ('phone', 2600)")
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


def get_product_by_id(product_id):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    results = cur.execute("SELECT * FROM products WHERE id = '{}'".format(product_id))
    res = results.fetchone()
    con.close()
    if res:
        product = {'id': res[0], 'name': res[1], 'price': res[2]}
        return product
    else:
        return None


def get_products():
    con = sql.connect(DATABASE)
    cur = con.cursor()
    results = cur.execute("SELECT * FROM products")
    items = []
    for row in results:
        items.append({'id': row[0], 'name': row[1], 'price': row[2]})
    con.close()
    return items


def insert_order(date, cost, items, user_id):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO orders (date, cost, items, user_id) VALUES ('{}', '{}', '{}', {})".format(date, cost, items, user_id))
    con.commit()
    con.close()


def get_orders_by_id(user_id):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    results = cur.execute("SELECT * FROM orders WHERE user_id = '{}'".format(user_id))
    order_list = []
    for row in results:
        order_list.append({'date': row[1], 'cost': row[2], 'items': row[3]})
    con.close()
    return order_list
