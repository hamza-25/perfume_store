from flask import Flask, render_template
from db_info import USER, PASSWORD, DATABASE_NAME
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

# from flask_migrate import Migrate
# import dbStorage
# import mysql.connector




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:@localhost/{DATABASE_NAME}'
db = SQLAlchemy(app)
from models import Category, Product, Address, Order, User


@app.route('/')
def home():
    from models.Category import Category
    from models.Product import Product
    Session = db.session()
    pr = Session.query(Product).all()
    categories = Session.query(Category).all()
    return render_template('index.html', title='Home Page', pr=pr, categories=categories)

@app.route('/product/<int:id>')
def single_product(id):
    return render_template('single_product_page.html', title='product')

@app.route('/profil')
def profil():
    return render_template('profil.html', title='profil')


if __name__ == '__main__':
    app.run(debug=True)