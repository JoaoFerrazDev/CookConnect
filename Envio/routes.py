from flask import Blueprint, request, jsonify
from models import db, Shipment

shipping_blueprint = Blueprint('shipping', __name__, url_prefix='/api/shipping')


@shipping_blueprint.route('/create', methods=['POST'])
def create_shipment():
    data = request.get_json()
    order_id = data.get('order_id')
    tracking_number = data.get('tracking_number')
    shipping_address = data.get('shipping_address')

    if not order_id or not tracking_number or not shipping_address:
        return jsonify({"error": "Missing required fields"}), 400

    new_shipment = Shipment(
        order_id=order_id,
        tracking_number=tracking_number,
        status='Pending',
        shipping_address=shipping_address
    )

    db.session.add(new_shipment)
    db.session.commit()

    return jsonify({"message": "Shipment created", "shipment": new_shipment.id}), 201


@shipping_blueprint.route('/update/<int:id>', methods=['POST'])
def update_shipment(id):
    shipment = Shipment.query.get_or_404(id)
    data = request.get_json()

    shipment.status = data.get('status', shipment.status)

    db.session.commit()

    return jsonify({"message": "Shipment updated", "shipment": shipment.id, "Status": shipment.status}), 200


@shipping_blueprint.route('/<int:id>', methods=['GET'])
def get_shipment(id):
    shipment = Shipment.query.get_or_404(id)
    return jsonify({
        "id": shipment.id,
        "order_id": shipment.order_id,
        "tracking_number": shipment.tracking_number,
        "status": shipment.status,
        "shipping_address": shipment.shipping_address,
        "created_at": shipment.created_at,
        "updated_at": shipment.updated_at
    }), 200
