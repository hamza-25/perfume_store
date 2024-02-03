from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    confirm_password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    email_verification = db.Column(db.String(30), nullable=True)
    is_admin = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    addresses = db.relationship('Address', backref='user_ref', lazy=True)
    orders = db.relationship('Order', backref='user_orders', lazy=True)


    # def __init__(self, first_name, last_name, password, confirm_password, email, email_verification, created_at, updated_at):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.password = password
    #     self.confirm_password = confirm_password
    #     self.email = email
    #     self.email_verification = email_verification
    #     self.created_at = created_at
    #     self.updated_at = updated_at
    
    
    