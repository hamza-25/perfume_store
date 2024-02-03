from app import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    products = db.relationship('Product', backref='category_ref', lazy=True)
    
    # def __init__(self, name):
    #     self.name = name