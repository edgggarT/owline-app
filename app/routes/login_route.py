from flask import Blueprint, request, jsonify   
from flask_jwt_extended import create_access_token
from ..database.users_db import users_db


login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': "Faltan correo o contraseña"}), 400
    
    user = users_db.find_user(email, password)

    if user:
        token = create_access_token(identity=str(user['id']))
        return jsonify({
            "message": "Login existoso",
            "token": token,
            "user_id": user['id'],
            "name": user['name']
        }), 200
    else:
        return jsonify({"message": "Credenciales incorrectas"})