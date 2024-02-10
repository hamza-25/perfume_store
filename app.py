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
    admin = is_admin()
    return render_template('single_product_page.html', admin=admin, title='product', product=product)

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
    from models.Category import Category
    if request.method == 'POST':
        name = request.form['name']
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('category'))
    categories = db.session.query(Category).all()
    return render_template('admin/category.html', categories=categories, title='category page')

@app.route("/admin/product", methods=['GET', 'POST'])
@login_required
def product():
    if not is_admin():
        return 'access denied'
    from models.Category import Category
    from models.Product import Product
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        discount_price = float(request.form['discount_price'])
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        category_id = int(request.form['category'])
        new_product = Product(discount_price=discount_price, title=title, description=description,
                              price=price, quantity=quantity, category_id=category_id)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('product'))
        
    products = db.session.query(Product).all()
    categories = db.session.query(Category).all()
    return render_template('admin/product.html', products=products, title="product page", categories=categories)

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

@app.route("/admin/user", methods=['GET', 'POST'])
@login_required
def user():
    if not is_admin():
        return 'access denied'
    if request.method == 'POST':
        pass
    from models.User import User
    users = db.session.query(User).filter_by(is_admin=None).all()
    return render_template('admin/user.html', users=users, title='users page')

@app.route('/user_orders')
@login_required
def user_orders():
    from models.Order import Order
    id = current_user.id
    orders = db.session.query(Order).filter_by(user_id=id).all()
    return render_template('orders.html', title='orders', orders=orders)


@app.route('/delete/order/<int:order_id>')
@login_required
def delete_order(order_id):
    from models.Order import Order
    id = current_user.id
    order = db.session.query(Order).filter_by(user_id=id, id=order_id).first()
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('user_orders'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if request.method == 'POST':
        quantity = request.form['quantity']
        if int(quantity) == 0:
            return redirect(url_for('home'))
        product_id = request.form['product_id']
        from models.Product import Product
        product = db.session.query(Product).filter_by(id=product_id).first()
        total = float(quantity) * float(product.price)
        return render_template('checkout_page.html', title="checkout page", total=total, product_id=product_id)
        
        
@app.route('/confirm_checkout', methods=['POST'])
@login_required
def confirm_checkout():
    if request.method == 'POST':
        street = request.form['street']
        country = request.form['country']
        state = request.form['state']
        city = request.form['city']
        zip = request.form['zip']
        user_id = current_user.id
        total = float(request.form['total'])
        product_id = int(request.form['product_id'])
        from models.Address import Address
        from models.Order import Order
        from datetime import datetime
        from random import randint
        transaction = f'{user_id}DFGF{randint(0, 10000)}'
        
        new_address = Address(user_id=user_id, city=city, zip=zip, state=state, country=country, street=street)
        new_order = Order(user_id=user_id, transaction=transaction, total_price=total, products_id=product_id, order_status='placed', ordered_at=datetime.now(), payement_method='Credit Card')
        db.session.add(new_address)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('user_orders'))
    return redirect(url_for('home'))
    
@app.route('/add-address', methods=['POST'])
@login_required
def add_address():
    if request.method == 'POST':
        street = request.form['street']
        country =  request.form['country']
        state =  request.form['state']
        city =  request.form['city']
        zip =  request.form['zip']
        from models.Address import Address
        try:
            new_address =  Address(street=street, country=country, city=city, zip=zip, state=state, user_id=current_user.id)
            db.session.add(new_address)
            db.session.commit()
        except Exception as e:
            pass
        return redirect(f'/profil/{current_user.id}')
    return render_template('index.html', title='home page')

@app.route('/delete/address/<int:id>', methods=['GET'])
@login_required
def delete_address(id):
    from models.Address import Address
    address = db.session.query(Address).filter_by(id=int(id)).first()
    if address.user_id == current_user.id:
        db.session.delete(address)
        db.session.commit()
        return redirect(f'/profil/{current_user.id}')
    return redirect('home')

@app.route('/edit/address/<int:id>', methods=['GET'])
@login_required
def edit_address(id):
    from models.Address import Address
    address = db.session.query(Address).filter_by(id=int(id)).first()
    if address.user_id == current_user.id:
        return render_template('edit_address.html', title='edit address', address=address)
    return redirect('home')

@app.route('/update/address', methods=['POST'])
@login_required
def update_address():
    if request.method == "POST":
        street = request.form['street']
        country = request.form['country']
        state = request.form['state']
        city = request.form['city']
        zip = request.form['zip']
        addr_id = request.form['addr_id']
        from models.Address import Address
        address = db.session.query(Address).filter_by(id=int(addr_id)).first()
        if address.user_id == current_user.id:
            address.country = country
            address.city = city
            address.state = state
            address.zip = zip
            address.street = street
            db.session.commit()
            return redirect(f'/profil/{current_user.id}')
    return redirect('home')
    

if __name__ == '__main__':
    app.run(debug=True)