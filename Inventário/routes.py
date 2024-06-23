from flask import Blueprint, jsonify, request
from models import Inventory, db

inventory_blueprint = Blueprint('inventory_api', __name__, url_prefix='/api/inventory')

@inventory_blueprint.route('/check/<product_id>', methods=['GET'])
def check_stock(product_id):
    inventory_item = Inventory.query.filter_by(product_id=product_id).first()
    if inventory_item:
        return jsonify({'stock_quantity': inventory_item.stock_quantity}), 200
    else:
        return jsonify({'message': 'Product not found.'}), 404

@inventory_blueprint.route('/update', methods=['POST'])
def update_stock():

    product_id = request.form['product_id']
    stock_quantity = request.form['stock_quantity']

    inventory_item = Inventory.query.filter_by(product_id=product_id).first()
    if inventory_item:
        inventory_item.stock_quantity = stock_quantity
        db.session.commit()
        return jsonify({'message': 'Stock updated successfully.'}), 200
    else:
        new_item = Inventory(product_id=product_id, stock_quantity=stock_quantity)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Stock added successfully.'}), 201

@inventory_blueprint.route('/reduce', methods=['POST'])
def reduce_stock():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    inventory_item = Inventory.query.filter_by(product_id=product_id).first()
    if inventory_item and inventory_item.stock_quantity >= quantity:
        inventory_item.stock_quantity -= quantity
        db.session.commit()
        return jsonify({'message': 'Stock reduced successfully.'}), 200
    elif not inventory_item:
        return jsonify({'message': 'Product not found.'}), 404
    else:
        return jsonify({'message': 'Insufficient stock.'}), 400
