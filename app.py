from flask import render_template, session, redirect, url_for, request
from func_bd import app, user, admin

# ! Основной код проекта
@app.route('/', methods = ["POST", "GET"])
def main():
    products = admin.bd_product.get_all_by_third_category_id(1)
    return render_template('main.html', products = products)

@app.route('/product/<int:product_id>')
def product(product_id = None):
    if product_id:
        products = admin.bd_product.get_by_id(product_id)
        comments = admin.bd_comment.get_by_product_id(product_id)
        len_comments = len(comments)
        return render_template('product.html', products=products, len_comments=len_comments, comments=comments)


@app.route('/catalog/')
@app.route('/catalog/<int:catalog_id>')
def catalog(catalog_id = None ):
    if catalog_id:
        catalogs = admin.bd_category.get_by_id(catalog_id)
        second_catalogs = admin.bd_second_category.get_by_category_id(catalog_id)
        return render_template('catalog.html', catalogs=catalogs, second_catalogs=second_catalogs)
    else:
        catalogs = admin.bd_category.get_all()
        # category_id = 1 популярные продукты
        
        second_catalogs = admin.bd_second_category.get_by_category_id(1)
        return render_template('catalog.html', catalogs=catalogs, second_catalogs=second_catalogs)

@app.route('/second_catalog/<int:second_catalog_id>')
def second_catalog(second_catalog_id):
    catalogs = admin.bd_second_category.get_by_id(second_catalog_id)
    second_catalogs = admin.bd_third_category.get_by_second_category_id(second_catalog_id)
    return render_template('catalog copy.html', catalogs=catalogs, second_catalogs=second_catalogs)

@app.route('/third_catalog/<int:third_catalog_id>')
def third_catalog(third_catalog_id):
    catalogs = admin.bd_third_category.get_by_id(third_catalog_id)
    products = admin.bd_product.get_all_by_third_category_id(third_catalog_id)
    return render_template('sale.html', catalogs=catalogs, products=products)
        

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if user.bd_user.login(password=password, username=username):
            human = user.bd_user.get_by_username(username=username)
            session['user_id'] = human.id
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('main'))

    return render_template('login.html')

@app.route('/register', methods = ["POST", "GET"])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        password_double = request.form.get('password_double')
        if password == password_double:
            if user.bd_user.registration(username=username, password=password, email=email, phone=phone):
                human = user.bd_user.get_by_username(username=username)
                session['user_id'] = human.id
                return redirect(url_for('profile'))
        
    return render_template('registration.html')

@app.route('/logout', methods = ["POST", "GET"])
def logout():
    
    session.clear()
                
        
    return redirect(url_for('main'))

@app.route('/profile', methods = ["POST", "GET"])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'change':
                first_name = request.form.get('first_name')
                username = request.form.get('username')
                phone = request.form.get('phone')
                email = request.form.get('email')
                user.bd_user.change_by_id(id = session['user_id'], username=username, first_name=first_name,
                                          phone=phone, email=email)
            if action == 'delete':
                user.bd_user.delete_by_id(session['user_id'])
                return redirect(url_for('logout'))
            if action == 'logout':
                return redirect(url_for('logout'))
            
        get_user = user.bd_user.get_by_id(session['user_id'])
    return render_template('profil.html', get_user=get_user)

@app.route('/favourites')
def favorite():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if not user.bd_favorite_product.get_by_user_id(session['user_id']):
            return render_template('favourites.html')
        else:
            favorite_product = user.bd_favorite_product.get_by_user_id(session['user_id'])
            return render_template('favourites copy.html', favorite_product=favorite_product)

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        pass
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(debug=True)
