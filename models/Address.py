from app import db

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    zip = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('addresses_ref', lazy=True))
    orders = db.relationship('Order', backref='order_ref', lazy=True)
    
    
    # def __init__(self, country, state, city, zip, street, user_id):
    #     self.country = country
    #     self.state = state
    #     self.city = city
    #     self.zip = zip
    #     self.street = street
    #     self.user_id = user_id