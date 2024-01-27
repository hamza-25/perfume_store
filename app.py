from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='Home Page')

@app.route('/product/<int:id>')
def single_product(id):
    return render_template('single_product_page.html', title='product')

if __name__ == '__main__':
    app.run(debug=True)