from flask import Flask, render_template
from db_info import USER, PASSWORD, DATABASE_NAME
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import dbStorage
import mysql.connector


    

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/perfume_db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class photos(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    def __init__(self, name):
        self.name = name

@app.route('/')
def home():
    # photo = photos('hamid')
    # db.session.add(photo)
    # db.session.commit()
    ph = db.session.execute(db.select(photos))
    def rows_to_dicts(cursor):
        # Fetch column names
        columns = [column[0] for column in cursor.description]

        # Fetch the results as dictionaries
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        return results
    # Connect to your MySQL server
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='perfume_db'
    )

    # Create a cursor object to execute SQL statements
    cursor = cnx.cursor()

    # Execute your SQL statement
    sql_statement = "SELECT * FROM products"
    cursor.execute(sql_statement)

    # Fetch the results
    results = rows_to_dicts(cursor)

    return render_template('index.html', title='Home Page', pr=results, ph=ph)

@app.route('/product/<int:id>')
def single_product(id):
    return render_template('single_product_page.html', title='product')

@app.route('/profil')
def profil():
    return render_template('profil.html', title='profil')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
# its important that because when we run the migration will detect our models
from models import User, Address, Category, Order, Product


