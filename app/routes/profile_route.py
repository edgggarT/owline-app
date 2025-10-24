from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..database.users_db import users_db


profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_info():
    user_id = get_jwt_identity()
    user = users_db.find_user_by_id(int(user_id))
    print(user_id)

    if not user:
        return jsonify({'msg':'Usuario no encontrado'}), 404
    
    return jsonify({
        'name': user['name'],
        'email': user['email']
    }), 200

@profile_bp.route('/profile', methods=['PATCH'])
@jwt_required()
def update_user_info():
    user_id = get_jwt_identity()
    data = request.get_json()

    user = users_db.find_user_by_id(int(user_id))
    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 404
    
    currentPassword = data.get('currentPassword')
    if not currentPassword:
        return jsonify({'msg': 'Contraseña actual incorrecta'}), 401
    
    updates = {}

    new_name = data.get('name')
    if new_name and new_name != user['name']:
        updates['name'] = new_name


    new_email = data.get('email')
    if new_email and new_email != user['email']:
        if users_db.email_exists(new_email, user_id):
            return jsonify({'msg': 'El email ya esta registrado'}), 500
        updates['email'] = new_email

    new_password = data.get('newPassword')
    confirm_password = data.get('confirmPassword')
    if new_password:
        if new_password != confirm_password:
            return jsonify({'msg': 'La nueva contraseña y la confirmacion no coincide'})
        updates['password'] = new_password

    if not updates:
        return jsonify({'msg': 'No hay campos validos para actualizar'}), 200
    
    if users_db.update_user_db(user_id, updates):
        return jsonify({
            'msg': 'Perfil actualizado con exito',
            'name': updates.get('name', user['name']),
            'email': updates.get('email', user['email']) 
        })









