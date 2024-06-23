from flask import Blueprint, jsonify, request, current_app
from models import Encomenda, EncomendaLinha, db
from flask import Flask
import requests

app = Flask(__name__)
encomenda_blueprint = Blueprint('encomenda_api_routes', __name__, url_prefix='/api/encomenda')
app.config['INVENTORY_SERVICE_URL'] = 'http://127.0.0.1:5005/api/inventory'

UTILIZADOR_API_URL = 'http://127.0.0.1:5001/api/utilizador'


def get_utilizador(api_key):
    headers = {
        'Authorization': api_key
    }
    response = requests.get(UTILIZADOR_API_URL, headers=headers)

    if response.status_code != 200:
        return {'message': 'Não autorizado 2.'}

    utilizador = response.json()
    return utilizador


@encomenda_blueprint.route('/', methods=['GET'])
def get_encomenda_pendente():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Não está autenticado.'}), 401
    response = get_utilizador(api_key)
    utilizador = response.get('result')
    if not utilizador:
        return jsonify({'message': 'Não está autenticado.'}), 401

    encomendaPendente = Encomenda.query.filter_by(utilizadorId=utilizador['id'], aberta=1).first()

    if encomendaPendente:
        return jsonify({'result': encomendaPendente.serializar()}), 200
    else:
        return jsonify({'message': 'Sem encomenda pendente.'})


@encomenda_blueprint.route('/all', methods=['GET'])
def get_todas_encomendas():
    encomendas = Encomenda.query.all()
    result = [encomenda.serializar() for encomenda in encomendas]
    return jsonify(result), 200


@encomenda_blueprint.route('/adicionarArtigo', methods=['POST'])
def adicionar_item_encomenda():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Não está autenticado 0.'}), 401
    response = get_utilizador(api_key)
    if not response.get('result'):
        return jsonify({'message': 'Não está autenticado 1.'}), 401
    utilizador = response.get('result')
    artigoId = int(request.form['artigoId'])
    quantidade = int(request.form['quantidade'])
    utilizadorId = utilizador['id']

    # Check stock level
    inventory_service_url = current_app.config['INVENTORY_SERVICE_URL'] + f'/check/{artigoId}'
    stock_response = requests.get(inventory_service_url)
    if stock_response.status_code != 200:
        return jsonify({'message': 'Failed to check stock level.'}), 500
    stock_quantity = stock_response.json().get('stock_quantity')
    if stock_quantity < quantidade:
        return jsonify({'message': 'Insufficient stock.'}), 400

    encomendaPendente = Encomenda.query.filter_by(utilizadorId=utilizadorId, aberta=1).first()

    if not encomendaPendente:
        encomendaPendente = Encomenda()
        encomendaPendente.aberta = True
        encomendaPendente.utilizadorId = utilizadorId

        linhaEncomenda = EncomendaLinha(artigoId=artigoId, quantidade=quantidade)
        encomendaPendente.linhas_encomenda.append(linhaEncomenda)
    else:
        encontrou = False
        for linha in encomendaPendente.linhas_encomenda:
            if linha.artigoId == artigoId:
                linha.quantidade += quantidade
                encontrou = True
        if not encontrou:
            linhaEncomenda = EncomendaLinha(artigoId=artigoId, quantidade=quantidade)
            encomendaPendente.linha_encomenda.append(linhaEncomenda)
    db.session.add(encomendaPendente)
    db.session.commit()

    return jsonify({'result': encomendaPendente.serializar()})

@encomenda_blueprint.route('/checkout/', methods=['POST'])
def checkout():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Não está autenticado.'}), 401
    response = get_utilizador(api_key)
    utilizador = response.get('result')
    if not utilizador:
        return jsonify({'message': 'Não está autenticado.'}), 401

    encomenda_pendente = Encomenda.query.filter_by(utilizadorId=utilizador['id'], aberta=1).first()

    if encomenda_pendente:
        # Reduce stock
        for linha in encomenda_pendente.linhas_encomenda:
            inventory_service_url = current_app.config['INVENTORY_SERVICE_URL'] + '/reduce'
            reduce_data = {
                "product_id": linha.artigoId,
                "quantity": linha.quantidade
            }
            reduce_response = requests.post(inventory_service_url, json=reduce_data)
            if reduce_response.status_code != 200:
                return jsonify({'message': 'Failed to reduce stock.'}), 500

        encomenda_pendente.aberta = False
        db.session.add(encomenda_pendente)
        db.session.commit()

        shipping_data = {
            "order_id": encomenda_pendente.id,
            "tracking_number": "TRK" + str(encomenda_pendente.id),
            "shipping_address": utilizador['address']  # Assuming the address is in the user data
        }
        shipping_service_url = current_app.config['SHIPPING_SERVICE_URL'] + '/create'
        shipping_response = requests.post(shipping_service_url, json=shipping_data)
        if shipping_response.status_code != 201:
            return jsonify({'message': 'Failed to create shipment.'}), 500

        return jsonify({'result': encomenda_pendente.serializar()})
    else:
        return jsonify({'message': 'Sem encomenda pendente.'})

@encomenda_blueprint.route('/historico', methods=['GET'])
def historico_encomendas():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Não está autenticado.'}), 401
    response = get_utilizador(api_key)
    utilizador = response.get('result')
    if not utilizador:
        return jsonify({'message': 'Não está autenticado.'}), 401

    encomendas = Encomenda.query.filter_by(utilizadorId=utilizador['id'], aberta=False).all()
    result = [encomenda.serializar() for encomenda in encomendas]
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True)
