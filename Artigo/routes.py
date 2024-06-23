from flask import Blueprint, request, jsonify, current_app
from models import Artigo, db
import requests

artigo_blueprint = Blueprint('artigo_api_routes', __name__, url_prefix='/api/artigo')


@artigo_blueprint.route('/todos', methods=['GET'])
def get_todos_artigos():
    todos_artigos = Artigo.query.all()
    result = [artigo.serializar() for artigo in todos_artigos]
    response = {"result": result}
    return jsonify(response)


@artigo_blueprint.route('/criar', methods=['POST'])
def criar_artigos():
    try:
        artigo = Artigo()
        artigo.descricao = request.form['descricao']
        artigo.codigoArtigo = request.form['codigoArtigo']
        artigo.imagem = request.form['imagem']
        artigo.preco = request.form['preco']

        db.session.add(artigo)
        db.session.commit()

        # Add the new product to the inventory
        inventory_service_url = current_app.config['INVENTORY_SERVICE_URL'] + '/update'
        inventory_data = {
            'product_id': artigo.codigoArtigo,
            'stock_quantity': 0  # Initialize with 0 stock
        }
        inventory_response = requests.post(inventory_service_url, json=inventory_data)

        if inventory_response.status_code not in [200, 201]:
            return jsonify({'message': 'Erro ao adicionar artigo ao inventário.'}), inventory_response.status_code

        response = {'message': 'Artigo criado com sucesso.', 'result': artigo.serializar()}
    except Exception as e:
        print(str(e))
        response = {'message': 'Erro na criação do artigo.'}
    return jsonify(response)


@artigo_blueprint.route('/<cA>', methods=['GET'])
def detalhes_Artigo(cA):
    artigo = Artigo.query.filter_by(codigoArtigo=cA).first()
    if artigo:
        response = {'result': artigo.serializar()}
    else:
        response = {'message': 'Sem artigos criados.'}

    return jsonify(response)
