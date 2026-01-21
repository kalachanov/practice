from flask import render_template, session, redirect, url_for
from func_bd import app, user, admin

# ! Основной код проекта
@app.route('/', methods = ["POST", "GET"])
def main():
    products = admin.bd_product.get_all_by_third_category_id(1)
    return render_template('main.html', products = products)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def registration():
    return render_template('registration.html')

@app.route('/profil')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('registration'))
    return render_template('profil.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/favourites')
def favorite():
    return render_template('favourites.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(debug=True)
