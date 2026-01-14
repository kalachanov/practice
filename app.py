from flask import Flask
from flask import render_template
from func_bd import app, user, admin

# ! Основной код проекта
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main.html')
def main():
    return render_template('main.html')

@app.route('/catalog.html')
def catalog():
    return render_template('catalog.html')

@app.route('/favourites.html')
def favorite():
    return render_template('favorite.html')

if __name__ == '__main__':
    app.run()
