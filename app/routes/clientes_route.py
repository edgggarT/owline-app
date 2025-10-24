from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import emit
from ..database.clientes_db import clientes_db
from app import socketio


clientes_bp = Blueprint('clientes', __name__)


@clientes_bp.route('/clientDni', methods=['GET'])
def get_client_id():
    dniSearch = request.args.get('dni')

    if not dniSearch:
        return jsonify({'msg': 'Falta el parametro DNI'}), 400

    data = clientes_db.find_client_by_dni(dniSearch)
    print(dniSearch)

    if not data:
        return jsonify({'msg': 'Usuario no encontrado'}), 400

    return jsonify({
        'nombre': data['nombre'],
        'apellido': data['apellido'],
        'telefono': data['telefono'],
        'dni': data['dni'],
        'email': data['email'],
        'fecha_nacimiento': data['fecha_nacimiento'],
        'direccion_ciudad': data['direccion_ciudad'],
        'direccion_calle': data['direccion_calle'],
        'fecha_registro': data['fecha_creacion'],
    })

@clientes_bp.route('/clientRange', methods=['GET'])
def get_client_range():
    fechaInicial = request.args.get('fechaInicial')
    fechaFinal = request.args.get('fechaFinal')

    if not fechaInicial and fechaFinal:
        return jsonify({'msg': 'Falta los parametros de fecha'}), 400

    data = clientes_db.find_client_by_range(fechaInicial, fechaFinal)
    print(fechaInicial)
    print(fechaFinal)

    if not data:
        return jsonify({'msg': 'Usuario o usuarios no encontrados'}), 400

    print(data)

    return jsonify(data)


@clientes_bp.route('/logs', methods=['GET'])
def get_logs():
    logs = clientes_db.get_clients_logs()

    if not logs:
        jsonify({'msg': 'Logs no encontrados'})

    print(logs)
    return jsonify(logs)


@clientes_bp.route('/client', methods=['POST'])
@jwt_required()
def create_client():
    data = request.get_json()
    usuario_id = get_jwt_identity()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    dni = data.get('dni')
    telefono = data.get('telefono')
    fecha_nacimiento = data.get('fecha_nacimiento')
    direccion_ciudad = data.get('direccion_ciudad')
    direccion_calle = data.get('direccion_calle')

    if clientes_db.dni_exists(dni):
        return jsonify({'msg':'El DNI ya esta registrado'}), 409
    elif clientes_db.email_exists(email):
        return jsonify({'msg': 'El email ya esta registrado'}), 409
    else:
        success = clientes_db.create_client(usuario_id ,nombre, apellido, email, telefono, dni, fecha_nacimiento, direccion_ciudad, direccion_calle)
        
        if success:
            socketio.emit('Log actualizado', {'message':'Nuevo cliente creado'})
            return jsonify({'msg': 'Cliente registrado exitosamente'}), 200
        else:
            return jsonify({'msg': 'Ha ocurrido un error del servidor, intentelo mas tarde :('})

    

@clientes_bp.route('/client', methods=['DELETE'])
@jwt_required()
def delete_clients():
    usuario_id = get_jwt_identity()
    dniSearch = request.args.get('dni')
    print(dniSearch)

    if not dniSearch:
        return jsonify({'msg': 'No se encontro el dni'})
    
    remove = clientes_db.delete_client(usuario_id ,dniSearch)

    if remove:
        socketio.emit('Log actualizado', {'message':'Cliente eliminado'})
        print('Se elimino el cliente')
        return jsonify({'msg': 'Se elimino correctamente el cliente'})
    else:
        print('Error en la base de datos')
        return jsonify({'msg': 'Error en la BD'})


@clientes_bp.route('/client', methods=['PATCH'])
@jwt_required()
def update_client():
    usuario_id = get_jwt_identity()
    data = request.get_json()
    dniToUpdate = data.get('dni')
    updates = data.get('updates')

    if not dniToUpdate or not updates:
        return jsonify({'msg': 'Datos faltantes'})

    success = clientes_db.update_client_db(usuario_id ,dniToUpdate, updates)

    if success == 'sucess':
        socketio.emit('Log actualizado', {'message':'Cliente actualizado'})
        return jsonify({'msg': f'Cliente con DNI {dniToUpdate} actualizado'}), 200
    elif success == 'duplicate_email':
        return jsonify({'msg': f'El email ya esta registrado'}), 409
    else:
        return jsonify({'msg': f'Error al actualizar el cliente'}), 400

    