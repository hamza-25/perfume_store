from app import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float)
    quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products_ref', lazy=True))
    
    # def __init__(self, title, description, price, discount_price, quantity, category_id):
    #     self.title = title
    #     self.description = description
    #     self.price = price
    #     self.discount_price = discount_price
    #     self.quantity = quantity
    #     self.category_id = category_id