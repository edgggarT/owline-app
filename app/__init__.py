from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from datetime import timedelta
from .database import db_close

socketio = SocketIO()

def Create_app():
    app = Flask(__name__)

    app.config["JWT_COOKIE_CSRF_PROTECT"] = False 
    jwt_key = os.environ.get('JWT_SECRET_KEY')
    app.config["JWT_SECRET_KEY"] = jwt_key
    print(jwt_key)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)


    socketio.init_app(app, cors_allowed_origins='*')
    CORS(app)
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    @jwt.invalid_token_loader
    def custom_error(reason):
        print(f"DEBUG JWT: {reason}\n")
        return jsonify(msg=f"Autenticacion fallida: {reason}"), 401

    from .routes import api_bp
    app.register_blueprint(api_bp)


    app.teardown_appcontext(db_close)


    @app.route('/')
    def index():
        return 'Backend funcionando'
    
    return app, socketio
