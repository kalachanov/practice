from flask import Flask
from flask import render_template
from func_bd import app, user, admin

# ! Основной код проекта
@app.route('/', methods = ["POST", "GET"])
def main():
    products = admin.bd_product.get_all_by_third_category_id(1)
    return render_template('main_flask.html', products = products)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def registration():
    return render_template('registration.html')

@app.route('/profil')
def profile():
    return render_template('profil.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/favourites')
def favorite():
    return render_template('favorite.html')

if __name__ == '__main__':
    app.run(debug=True)
