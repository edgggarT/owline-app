from flask import Blueprint, jsonify, request
from ..database.users_db import users_db

register_bp = Blueprint('register', __name__)


@register_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if users_db.email_exists_register(email):
        return jsonify({'msg': 'El email ya existe!'})
    else:
        users_db.user_register(name, email, password)
    
    return jsonify({'msg': 'Error interno del servicio al registrar, intentelo mas tarde :('})