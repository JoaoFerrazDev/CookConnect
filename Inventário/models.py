from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.app = app
    db.init_app(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, unique=True, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, product_id, stock_quantity):
        self.product_id = product_id
        self.stock_quantity = stock_quantity

    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'stock_quantity': self.stock_quantity
        }
