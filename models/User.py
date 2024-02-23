from app import db
# from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    confirm_password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    email_verification = db.Column(db.String(128), nullable=True)
    is_admin = db.Column(db.Integer)
    is_ban = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    addresses = db.relationship('Address', backref='user_ref', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user_orders', lazy=True, cascade='all, delete-orphan')


    # def __init__(self, first_name, last_name, password, confirm_password, email, email_verification):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.password = password
    #     self.confirm_password = confirm_password
    #     self.email = email
    #     self.email_verification = email_verification
    #     self.created_at = datetime.now()
    #     self.updated_at = datetime.now()
    def __repr__(self):
        return '<User %r>' % self.username
    
    
    