from flask import Blueprint, jsonify, request, make_response
from models import db, Utilizador
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

utilizador_blueprint = Blueprint('utilizador_api_routes', __name__, url_prefix='/api/utilizador')


@utilizador_blueprint.route('/todos', methods=['GET'])
def get_Todos_Utilizadores():
    todosUtilizadores = Utilizador.query.all()
    result = [utilizador.serializar() for utilizador in todosUtilizadores]
    response = {
        'message': 'Todos os utilizadores',
        'result': result
    }
    return jsonify(response)


@utilizador_blueprint.route('/criar', methods=['POST'])
def criar_utilizador():
    try:
        nome_utilizador = request.form.get('nomeUtilizador')
        email = request.form.get('email')
        password = request.form.get('password')

        if not nome_utilizador or not email or not password:
            response = {'message': 'Nome de Utilizador, email e senha são obrigatórios.'}
            return jsonify(response), 400

        utilizador = Utilizador(
            nomeUtilizador=nome_utilizador,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            administrador=False
        )
        db.session.add(utilizador)
        db.session.commit()

        response = {
            'message': 'Utilizador criado com sucesso.',
            'result': utilizador.serializar()
        }
    except Exception as e:
        print(str(e))
        response = {'message': 'Erro na criação de utilizador.'}

    return jsonify(response)

@utilizador_blueprint.route('/login', methods=['POST'])
def login():
    nomeUtilizador = request.form['nomeUtilizador']
    password = request.form['password']

    utilizador = Utilizador.query.filter_by(nomeUtilizador=nomeUtilizador).first()
    if not utilizador:
        response = {'message': 'Este utilizador não existe.'}
        return make_response(jsonify(response), 401)

    if check_password_hash(utilizador.password, password):
        utilizador.update_api_key()
        utilizador.ativo = True  # Set ativo to True when user logs in
        db.session.commit()
        login_user(utilizador)
        response = {'message': 'Conectado', 'api_key': utilizador.api_key}
        return make_response(jsonify(response), 200)

    response = {'message': 'Autenticação incorreta.'}
    return make_response(jsonify(response), 401)


@utilizador_blueprint.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        current_user.ativo = False  # Set ativo to False when user logs out
        db.session.commit()
        logout_user()
        return jsonify({'message': 'Desconectado.'})
    return jsonify({'message': 'Não existem utilizadores conectados.'})


@utilizador_blueprint.route('/<nomeUtilizador>/existe', methods=['GET'])
def get_Utilizador_Existe(nomeUtilizador):
    utilizador = Utilizador.query.filter_by(nomeUtilizador=nomeUtilizador).first()
    if utilizador:
        return jsonify({'message': True}), 200

    return jsonify({'message: False'}), 404


@utilizador_blueprint.route('/', methods=['GET'])
def get_Utilizador_Atual():
    if current_user.is_authenticated:
        return jsonify({'result': current_user.serializar()}), 200
    else:
        return jsonify({'message': 'Utilizador não conectado.'}), 401
