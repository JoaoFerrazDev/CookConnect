from flask import Blueprint, request, jsonify
from models import Artigo, db

artigo_blueprint = Blueprint('artigo_api_routes', __name__, url_prefix='/api/artigo')


@artigo_blueprint.route('/todos', methods=['GET'])
def get_todos_artigos():
    todos_artigos = Artigo.query.all()
    result = [artigo.serializar() for artigo in todos_artigos]
    response = {"result":result}
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
        
        response = {'message': 'Artigo criado com sucesso.', 'result': artigo.serializar()}
    except Exception as e:
        print(str(e))
        response = {'message': 'Erro na criação do artigo.'}
    return jsonify(response)

@artigo_blueprint.route('/<cA>', methods=['GET'])
def detalhes_Artigo(cA):
    artigo = Artigo.query.filter_by(codigoArtigo=cA).first()
    if artigo:
        response={'result':artigo.serializar()}
    else:
        response={'message':'Sem artigos criados.'}
    
    return jsonify(response)