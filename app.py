from flask import render_template, session, redirect, url_for
from func_bd import app, user, admin

# ! Основной код проекта
@app.route('/', methods = ["POST", "GET"])
def main():
    products = admin.bd_product.get_all_by_third_category_id(1)
    return render_template('main.html', products = products)

@app.route('/catalog/')
@app.route('/catalog/<int:catalog_id>')
def catalog(catalog_id = None):
    if catalog_id:
        catalogs = admin.bd_category.get_by_id(catalog_id)
        second_catalogs = admin.bd_second_category.get_by_category_id(catalog_id)
        return render_template('catalog.html', catalogs=catalogs, second_catalogs=second_catalogs)
    else:
        catalogs = admin.bd_category.get_all()
        # category_id = 1 популярные продукты
        second_catalogs = admin.bd_second_category.get_by_category_id(1)
        return render_template('catalog.html', catalogs=catalogs, second_catalogs=second_catalogs)
        

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def registration():
    return render_template('registration.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profil.html')

@app.route('/favourites')
def favorite():
    return render_template('favourites.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(debug=True)
