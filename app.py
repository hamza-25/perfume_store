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
# login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from models.User import User
    return db.session.query(User).filter_by(id=user_id).first()

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
@login_required
def profil(id):
    from models.User import User
    user = get_profil_by_id(User, db, int(id))
    return render_template('profil.html', title='profil', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
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
        return render_template("test.html")
        # return redirect(url_for('home'))
    return render_template('register.html', title="register page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        from models.User import User

        # user = User.query.filter_by(email=email).first()  # Query the user from the database by username
        user = db.session.query(User).filter_by(email=email).first() # Query the user from the database by username


        # if user and check_password_hash(user.password, password):  # Check if the user exists and the password is correct
        #     login_user(user)  # Log in the user using Flask-Login
        #     return redirect(url_for('home'))  # Redirect to the home page after successful login
        if user: # Check if the user exists and the password is correct
            if password == user.password:
                login_user(user) 
                return redirect(url_for('home')) 
            else:
                return 'Invalid username or password'  # Display error message for invalid credentials

    return render_template('login.html')  # Render the login form

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)