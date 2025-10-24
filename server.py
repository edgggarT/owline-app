import os
from dotenv import load_dotenv

load_dotenv()

from app import Create_app

app, socketio = Create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)