from app import db
from sqlalchemy.orm import relationship, backref

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float)
    quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', backref('products'))
    
    def __init__(self, title, description, price, discount_price, quantity, category_id):
        self.title = title
        self.description = description
        self.price = price
        self.discount_price = discount_price
        self.quantity = quantity
        self.category_id = category_id