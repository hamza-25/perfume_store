from app import db
from sqlalchemy.dialects.mysql import JSON

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    transaction = db.Column(db.String(30), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    products_id = db.Column(db.String(128), nullable=False)
    products_id_json = db.Column(JSON, nullable=True)
    order_status = db.Column(db.String(30), nullable=False)
    ordered_at = db.Column(db.DateTime, nullable=False)
    payement_method = db.Column(db.String(30), nullable=False)
    address_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders_user', lazy=True))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    
 

    
    # def __init__(self, transaction, total_price, products_id, order_status, ordered_at, payement_method, user_id):
    #     self.transaction = transaction
    #     self.total_price = total_price
    #     self.products_id = products_id
    #     self.order_status = order_status
    #     self.ordered_at = ordered_at
    #     self.payement_method = payement_method
    #     self.user_id = user_id