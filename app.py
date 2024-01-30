from flask import Flask, render_template
from db_info import USER, PASSWORD, DATABASE_NAME
from flask_sqlalchemy import SQLAlchemy
# from models import User, Address, Category, Order, Product
# from models import Category
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/perfume_db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    # engine = create_engine("mysql+pymysql://root:@localhost/perfume_db")
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # from models import Product
    # all_products = Product.query.all()
    # return all_products
    return render_template('index.html', title='Home Page')

@app.route('/product/<int:id>')
def single_product(id):
    return render_template('single_product_page.html', title='product')

@app.route('/profil')
def profil():
    return render_template('profil.html', title='profil')


if __name__ == '__main__':
    app.run(debug=True)
    
# its important that because when we run the migration will detect our models
from models import User, Address, Category, Order, Product

