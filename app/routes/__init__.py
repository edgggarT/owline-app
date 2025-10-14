from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

from .login_route import login_bp

api_bp.register_blueprint(login_bp, url_prefix='/auth')

from .profile_route import profile_bp

api_bp.register_blueprint(profile_bp, url_prefix='/user')

from .register_route import register_bp

api_bp.register_blueprint(register_bp, url_prefix='/auth')

from .clientes_route import clientes_bp

api_bp.register_blueprint(clientes_bp, url_prefix='/clients')