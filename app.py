from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from db_info import USER, PASSWORD, DATABASE_NAME
from flask_migrate import Migrate
from flask_cors import CORS
# blueprint register
# from admin_route import admin_page

# app config
app = Flask(__name__)
# app.register_blueprint(admin_page, url_prefix='/admin')
app.config['SECRET_KEY'] = '44e2168417769a72e6e03174e6b4209841b5d2dd13f89794df8ef2f32a2f4f90'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:@localhost/{DATABASE_NAME}'
app.config['UPLOAD_FOLDER'] = 'static/images/uploads/'

db = SQLAlchemy(app)


migrate = Migrate(app, db)
CORS(app)



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
        
@app.before_request
def check_user_ban():
    if current_user.is_authenticated and current_user.is_ban:
        logout_user()  # Assuming you're using Flask-Login for user authentication
        return redirect(url_for('login'))

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

@app.route('/profil/<int:id>', methods=['GET', 'POST'])
@login_required
def profil(id):
    from models.User import User
    from form_validator.profilForm import ProfilFrom
    form = ProfilFrom(request.form)
    # hanlde post request
    if request.method == 'POST' and form.validate():
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        user = get_profil_by_id(User, db, int(id))
        user.email = email
        user.first_name = fname
        user.last_name = lname
        user.updated_at = datetime.now()
        db.session.commit()
        flash('profil updated successfully', 'successfully')
        return redirect(f'/profil/{id}')
    
    # hanlde get request 
    user = get_profil_by_id(User, db, int(id))
    
    # set form to default values
    form.first_name.default = user.first_name
    form.last_name.default = user.last_name
    form.email.default = user.email
    return render_template('profil.html', title='profil', user=user, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    from form_validator.registerFrom import RegisterFrom
    form = RegisterFrom(request.form)
    # handle post request
    if request.method == 'POST' and form.validate():
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return 'password not match'
        hash_password = generate_password_hash(password)
        from models.User import User
        new_user = User(first_name=fname, last_name=lname, password=hash_password, confirm_password=hash_password, email=email, email_verification=email, created_at=datetime.now(), updated_at=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    # handle get request
    return render_template('register.html', title="register page", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    from form_validator.loginFrom import LoginFrom
    form = LoginFrom(request.form)
    # handle post request
    if request.method == 'POST' and form.validate():
        email = request.form['email']
        password = request.form['password']
        from models.User import User
        user = db.session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password): 
            login_user(user) 
            return redirect(url_for('home')) 
        else:
            flash('Email or Password incorrect !')  
    # handle get request
    return render_template('login.html', form=form)

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
    from form_validator.categoryForm import CategoryFrom
    form = CategoryFrom(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully', 'success')
        return redirect(url_for('category'))
    categories = db.session.query(Category).all()
    return render_template('admin/category.html', categories=categories, title='category page', form=form)

@app.route('/admin/edit/category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    if not is_admin():
        return 'access denied'
    from models.Category import Category
    category = db.session.query(Category).filter_by(id=id).first()
    if request.method == 'POST':
        category_name = request.form['category_name']
        category.name = category_name
        db.session.commit()
        flash('Category updated successfully', 'success')
        return redirect(url_for('category'))
    return render_template('admin/edit_category.html', title='edit category', category=category)

@app.route('/admin/delete/category/<int:id>')
def delete_category(id):
    if not is_admin():
        return 'access denied'
    from models.Category import Category
    category = db.session.query(Category).filter_by(id=id).first()
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully', 'error')
    return redirect(url_for('category'))

@app.route("/admin/product", methods=['GET', 'POST'])
@login_required
def product():
    if not is_admin():
        return 'access denied'
    from models.Category import Category
    from models.Product import Product
    from form_validator.productForm import ProductForm
    form = ProductForm(request.form)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        discount_price = float(request.form['discount_price'])
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        category_id = int(request.form['category'])
        
        file = request.files['file']
        import uuid, os
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        file.save(os.path.join('static/images/uploads', filename))
        
        new_product = Product(discount_price=discount_price, title=title, description=description,
                              price=price, quantity=quantity, category_id=category_id, image=filename)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully', 'successfully')
        return redirect(url_for('product'))
        
    products = db.session.query(Product).all()
    categories = db.session.query(Category).all()
    return render_template('admin/product.html', products=products, title="product page", categories=categories, form=form)


@app.route("/admin/edit/product/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if not is_admin():
        return 'access denied'
    from models.Product import Product
    product = get_product_by_id(Product, db, id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        discount_price = float(request.form['discount_price'])
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        category_id = int(request.form['category'])
        product.title = title
        product.description = description
        product.discount_price = discount_price
        product.price = price
        product.quantity = quantity
        product.category_id = category_id
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('product'))
        
    from models.Category import Category
    categories = get_all(Category, db)
    return render_template('admin/edit_product.html', product=product, title='edit product', categories=categories)
    


@app.route("/admin/delete/product/<int:id>", methods=['GET'])
@login_required
def delete_product(id):
    from models.Product import Product
    product = db.session.query(Product).filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'successfully')
    return redirect(url_for('product'))


@app.route("/admin/order", methods=['GET', 'POST'])
@login_required
def order():
    if not is_admin():
        return 'access denied'
    from models.Order import Order
    orders = get_all(Order, db)
    return render_template('admin/order.html', orders=orders, title='order page')

@app.route("/admin/delete/order/<int:id>", methods=['GET'])
@login_required
def admin_delete_order(id):
    if not is_admin():
        return 'access denied'
    from models.Order import Order
    order = db.session.query(Order).filter_by(id=id).first()
    db.session.delete(order)
    db.session.commit()
    flash('order deleted successfully', 'successfully')
    return redirect(url_for('order'))


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

@app.route("/admin/delete/user/<int:id>", methods=['GET'])
@login_required
def admin_delete_user(id):
    if not is_admin():
        return 'access denied'
    from models.User import User
    user = db.session.query(User).filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    flash('user deleted successfully', 'successfully')
    return redirect(url_for('user'))

@app.route('/admin/user/ban/<int:id>')
def ban_user(id):
    if not is_admin():
        return 'access denied'
    from models.User import User
    user = get_user_by_id(User, db, id)
    user.is_ban = 1
    db.session.commit()
    flash('user banned successfully', 'successfully')
    return redirect(url_for('user'))

@app.route('/admin/user/remove_ban/<int:id>')
def remove_ban_user(id):
    if not is_admin():
        return 'access denied'
    from models.User import User
    user = get_user_by_id(User, db, id)
    user.is_ban = 0
    db.session.commit()
    flash('user ban removed successfully', 'successfully')
    return redirect(url_for('user'))


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
    flash('order deleted successfully')
    return redirect(url_for('user_orders'))

@app.route('/delivered/order/<int:order_id>')
@login_required
def delivered(order_id):
    from models.Order import Order
    id = current_user.id
    order = db.session.query(Order).filter_by(user_id=id, id=order_id).first()
    order.order_status = 'delivered'
    db.session.commit()
    flash('order status change to delivered')
    return redirect(url_for('user_orders'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if request.method == 'POST':
        quantity = request.form['quantity']
        # if user forget to set quantity we set to 1 as default
        if  quantity == '':
            quantity = 1
        
        if int(quantity) == 0:
            return redirect(url_for('home'))
        product_id = request.form['product_id']
        from models.Product import Product
        product = db.session.query(Product).filter_by(id=product_id).first()
        total = float(quantity) * float(product.price)
        from models.User import User
        user = get_user_by_id(User, db, current_user.id)
        return render_template('checkout_page.html', user=user, title="checkout page", total=total, product_id=product_id)
        
        
@app.route('/confirm_checkout', methods=['POST'])
@login_required
def confirm_checkout():
    from form_validator.checkForm import CheckForm
    form = CheckForm(request.form)
    if request.method == 'POST' and form.validate():
        address_id = request.form['address']
        user_id = current_user.id

        # check if address belongs to current user
        valide_address_user = False
        for address in current_user.addresses:
            if int(address_id) == int(address.id):
                valide_address_user = True
        if not valide_address_user:
            flash('invalid address please use use valid one')
            return redirect(f'/profil/{current_user.id}')

        total = float(request.form['total'])
        product_id = int(request.form['product_id'])
        from models.Order import Order
        from datetime import datetime
        from random import randint
        transaction = f'{user_id}DFGF{randint(0, 10000)}'
        new_order = Order(address_id=address_id, user_id=user_id, transaction=transaction, total_price=total, products_id=product_id, order_status='placed', ordered_at=datetime.now(), payement_method='cash on delivery')
        db.session.add(new_order)
        db.session.commit()
        flash('order has successfully placed')
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
        full_name = request.form['full_name']
        from models.Address import Address
        try:
            new_address =  Address(full_name=full_name, street=street, country=country, city=city, zip=zip, state=state, user_id=current_user.id)
            db.session.add(new_address)
            db.session.commit()
        except Exception as e:
            pass
        flash('address added successfully')
        return redirect(f'/profil/{current_user.id}')
    return redirect(f'/profil/{current_user.id}')


@app.route('/delete/address/<int:id>', methods=['GET'])
@login_required
def delete_address(id):
    from models.Address import Address
    address = db.session.query(Address).filter_by(id=int(id)).first()
    if address.user_id == current_user.id:
        db.session.delete(address)
        db.session.commit()
        flash('address deleted successfully')
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
        full_name = request.form['full_name']
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
            address.full_name = full_name
            db.session.commit()
            flash('address updated successfully')
            return redirect(f'/profil/{current_user.id}')
    return redirect(f'/profil/{current_user.id}')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        admin = is_admin()
        search_input = request.form['search']
        category = request.form['category']
        from models.Product import Product
        from models.Category import Category
        if category == 'none':
            products = db.session.query(Product).filter(Product.title.like(f'%{search_input}%')).all()
            categories = get_all(Category, db)
            return render_template('index.html', title='Home Page', pr=products, categories=categories, admin=admin)
        else:
            #  return category
             products = db.session.query(Product).filter_by(category_id=category).filter(Product.title.like(f'%{search_input}%')).all()
             categories = get_all(Category, db)
             return render_template('index.html', title='Home Page', pr=products, categories=categories, admin=admin)
    
    return redirect(url_for('home'))  

if __name__ == '__main__':
    app.run(debug=True)