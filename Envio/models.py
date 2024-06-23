from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.app = app
    db.init_app(app)

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    tracking_number = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    shipping_address = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, order_id, tracking_number, status, shipping_address):
        self.order_id = order_id
        self.tracking_number = tracking_number
        self.status = status
        self.shipping_address = shipping_address
