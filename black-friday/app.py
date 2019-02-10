#! /usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import database as db
import datetime


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
            session['cart'] = []
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
    if 'cart' in session:
        session.pop('cart')
    return redirect(url_for('index'))


@app.route('/cart')
@login_required
def cart():
    cart_contents = get_cart(session['cart'])
    total = 0
    for item in cart_contents:
        total += item['product_total']
    args = {'active': 'cart', 'cart': cart_contents, 'total': total}
    return render_template('cart.html', args=args)


@app.route('/products')
def products():
    args = {'active': 'products', 'products': db.get_products()}
    return render_template('products.html', args=args)


def get_cart(product_ids):
    if not product_ids:
        return product_ids
    products = list()
    for product_id, product_qty in product_ids:
        product = db.get_product_by_id(product_id)
        if product:
            product['quantity'] = product_qty
            product['product_total'] = product['price'] * product_qty
            products.append(product)
    return products


@app.route('/addcart', methods=['POST'])
@login_required
def addcart():
    item_id = request.form['id']
    item_qty = int(request.form['quantity'])
    new_item = (item_id, item_qty)
    for item in session['cart']:
        if item[0] == item_id:
            new_item = (item_id, item[1] + item_qty)
        break
    new_cart = [item for item in session['cart'] if item[0] != item_id]
    session['cart'] = new_cart
    session['cart'].append(new_item)
    session.modified = True
    return redirect(url_for('cart'))


@app.route('/remcart', methods=['POST'])
@login_required
def remcart():
    item_id = request.form['id']
    new_cart = [item for item in session['cart'] if item[0] != item_id]
    session['cart'] = new_cart
    session.modified = True
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_contents = get_cart(session['cart'])
    if not cart_contents:
        flash('You must have items in your cart to checkout!')
        return redirect(url_for('products'))

    items = cart_to_string(cart_contents)
    total = 0
    for item in cart_contents:
        total += item['product_total']

    if total > 0:
        flash('Oh No! Our Payment Processor is not working!')
        return redirect(url_for('cart'))
    else:
        db.insert_order(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), total, items, current_user.user_id)
        session['cart'] = []
        session.modified = True
        flash('Your Order Was Successful')
        return redirect(url_for('orders'))


def cart_to_string(cart_contents):
    strings = ''
    for item in cart_contents:
        strings += '{} x {}, '.format(item['quantity'], item['name'])
    return strings


@app.route('/orders')
@login_required
def orders():
    order_list = db.get_orders_by_id(current_user.user_id)

    args = {'active': 'orders', 'orders': order_list}
    return render_template('orders.html', args=args)


@login_manager.user_loader
def load_user(user_id):
        return db.get_user_by_id(user_id)


if __name__ == '__main__':
    db.initialize_db()
    app.run(host='0.0.0.0', debug=DEBUG)
