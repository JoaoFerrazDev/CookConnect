from flask import Blueprint, jsonify, request, make_response
from models import db, Utilizador
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

utilizador_blueprint = Blueprint('utilizador_api_routes', __name__, url_prefix='/api/utilizador')


@utilizador_blueprint.route('/')
def index():
    return 'Olá Turma'


@utilizador_blueprint.route('/todos', methods=['GET'])
def get_Todos_Utilizadores():
    todosUtilizadores = Utilizador.query.all()
    result = [utilizador.serializar() for utilizador in todosUtilizadores]
    response = {
        'message': 'Todos os Utilizadores',
        'result': result
    }
    return jsonify(response)


@utilizador_blueprint.route('/criar', methods=['POST'])
def criar_Utilizador():
    try:
        # Verificacdo se o nomeUtilizador e a password estdo presentes
        nomeUtilizador = request.form.get('nomeUtilizador')
        password = request.form.get('password')
        if not nomeUtilizador or not password:
            response = {'message': 'Nome de utilizador e senha são obrigatórios.'}
            return jsonify(response), 400

        utilizador = Utilizador()
        utilizador.nomeUtilizador = request.form['nomeUtilizador']
        utilizador.password = generate_password_hash(
            request. form[ 'password'],
            method = 'pbkdf2:sha256')
        utilizador.administrador = False

        db.session.add(utilizador)
        db.session.commit()
        response = {'message': 'Utilizador criado com sucesso.',
                    'result: ': utilizador.serializar()}
    except Exception as e:
        print(str(e))
        response = {'message': 'Erro na criagido do utilizador.'}
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
        db.session.commit()
        login_user(utilizador)
        response = {'message': 'Conectado', 'api_key': utilizador.api_key}
        return make_response(jsonify(response), 200)

    utilizador.update_api_key()
    db.session.commit()
    login_user(utilizador)
    response = {'message': 'Conectado', 'api_key': utilizador.api_key}
    return make_response(jsonify(response), 200)

    response = {'message:': 'Autenticação incorreta.'}
    return make_response(jsonify(response), 401)

@utilizador.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated():
        logout_user()
        return jsonify({'message': 'Desconectado'})
    return jsonify({'message': 'Não existem utilizadores conectados.'})

@utilizador_blueprint.route('/<nomeUtilizador>/existe', methods=['GET'])
def get_Utilizador_existe(nomeUtilizador):
    utilizador = Utilizador.query.filter_by(nomeUtilizador = nomeUtilizador).first()
    if utilizador:
        return jsonify({'message': True},200)
    return jsonify({'message': False},404)

@utilizador_blueprint.route('/', methods = ['GET'])
def get_Utilizador_Atual():
    if current_user.is_authenticated():
        return jsonify({'message': current_user.serializar()}), 200
    else:
        return jsonify({'message':'Utilizador não conectado'}),401


56




