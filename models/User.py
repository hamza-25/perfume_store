from app import db
from sqlalchemy.orm import relationship, backref

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String, nullable=False)
    confirm_password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)  # Assuming you're using a regular string for email
    email_verification = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    addresses = relationship('Address', backref('user'))
    orders = relationship('Order', backref('user'))

    
    
    