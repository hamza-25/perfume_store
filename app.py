from flask import Flask, render_template
from db_info import USER, PASSWORD, DATABASE_NAME
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# be attention connector is it installed
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASSWORD}@localhost/{DATABASE_NAME}'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html', title='Home Page')

@app.route('/product/<int:id>')
def single_product(id):
    return render_template('single_product_page.html', title='product')

@app.route('/profil')
def profil():
    return render_template('profil.html', title='profil')

if __name__ == '__main__':
    app.run(debug=True)