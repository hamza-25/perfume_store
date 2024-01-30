from app import db
from sqlalchemy.orm import relationship, backref

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    products = relationship('Product', backref('category'))