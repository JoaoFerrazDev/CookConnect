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
        # Verificação se o nomeUtilizador e a password estão presentes
        nomeUtilizador = request.form('')