from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product , Category
import app


class dbStorage():
    def __init__(self):
        try:
            engine = create_engine('mysql+pymysql://root:@localhost/perfume_db', echo=True)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        except Exception as e:
            return {"error": 2}
    
    def all(self):
        try:
            # products = self.session.query(Product).all()
            products = app.db.session.execute(app.db.select(Product).order_by(Product.title))
            return products
        except Exception as e:
            return {"error": 1}

# # Usage
# db1 = dbStorage()
# if db1.session:  # Ensure session is not None
#     pr = db1.all()
#     if pr:  # Ensure products are retrieved
#         for product in pr:
#             print(product)
#     else:
#         print("No products found.")
