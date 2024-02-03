from flask import Flask, render_template
from db_info import USER, PASSWORD, DATABASE_NAME
from flask_sqlalchemy import SQLAlchemy
from db_operation import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:@localhost/{DATABASE_NAME}'
db = SQLAlchemy(app)
from models import Category, Product, Address, Order, User


@app.route('/')
def home():
    from models.Category import Category
    from models.Product import Product
    pr = get_all(Product, db)
    categories = get_all(Category, db)
    return render_template('index.html', title='Home Page', pr=pr, categories=categories)

@app.route('/product/<int:id>')
def single_product(id):
    from models.Product import Product
    product = get_product_by_id(Product, db, int(id))
    return render_template('single_product_page.html', title='product', product=product)

@app.route('/profil/<int:id>')
def profil(id):
    from models.User import User
    user = get_profil_by_id(User, db, int(id))
    return render_template('profil.html', title='profil', user=user)


if __name__ == '__main__':
    app.run(debug=True)