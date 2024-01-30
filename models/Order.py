from app import db
from sqlalchemy.orm import relationship, backref

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    transaction = db.Column(db.String(30), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    products_id = db.Column(db.String(128), nullable=False)
    order_status = db.Column(db.String(30), nullable=False)
    ordered_at = db.Column(db.DateTime, nullable=False)
    payement_method = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref('orders'))