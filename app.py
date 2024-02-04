from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from db_info import USER, PASSWORD, DATABASE_NAME

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkeyformyapp'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:@localhost/{DATABASE_NAME}'
db = SQLAlchemy(app)

from models import Category, Product, Address, Order, User
from db_operation import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from models.User import User
    return db.session.query(User).filter_by(id=user_id).first()

def is_admin():
    if current_user.is_authenticated:
        from models.User import User
        user = db.session.query(User).filter_by(id=current_user.id, is_admin=True).first()
        if not user:
            return False
        return True
    else:
        False
    
        

@app.route('/')
def home():
    from models.Category import Category
    from models.Product import Product
    pr = get_all(Product, db)
    categories = get_all(Category, db)
    admin = is_admin()
    return render_template('index.html', title='Home Page', pr=pr, categories=categories, admin=admin)

@app.route('/product/<int:id>')
def single_product(id):
    from models.Product import Product
    product = get_product_by_id(Product, db, int(id))
    return render_template('single_product_page.html', title='product', product=product)

@app.route('/profil/<int:id>')
@login_required
def profil(id):
    from models.User import User
    user = get_profil_by_id(User, db, int(id))
    return render_template('profil.html', title='profil', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return 'password not match'
        # hash_password = generate_password_hash(password)
        from models.User import User
        new_user = User(first_name=fname, last_name=lname, password=password, confirm_password=password, email=email, email_verification=email, created_at=datetime.now(), updated_at=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html', title="register page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        from models.User import User
        user = db.session.query(User).filter_by(email=email).first()
        if user: 
            if password == user.password:
                login_user(user) 
                return redirect(url_for('home')) 
            else:
                return 'Invalid username or password'  
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/admin")
@login_required
def home_admin():
    if not is_admin():
        return 'access denied'
    return render_template('admin/base_admin.html', title='admin page')

@app.route("/admin/category", methods=['GET', 'POST'])
@login_required
def category():
    if not is_admin():
        return 'access denied'
    if request.method == 'POST':
        pass
    from models.Category import Category
    categories = db.session.query(Category).all()
    return render_template('admin/category.html', categories=categories, title='category page')

@app.route("/admin/product", methods=['GET', 'POST'])
@login_required
def product():
    if not is_admin():
        return 'access denied'
    if request.method == 'POST':
        pass
    from models.Product import Product
    products = db.session.query(Product).all()
    return render_template('admin/product.html', products=products, title="product page")

@app.route("/admin/order", methods=['GET', 'POST'])
@login_required
def order():
    if not is_admin():
        return 'access denied'
    if request.method == 'POST':
        pass
    from models.Order import Order
    orders = db.session.query(Order).all()
    return render_template('admin/order.html', orders=orders, title='order page')

if __name__ == '__main__':
    app.run(debug=True)