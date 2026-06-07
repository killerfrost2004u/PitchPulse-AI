from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pitchpulse_secret_dev'
    
    # Initialize SocketIO, allowing cross-origin from frontend
    socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet')
    
    from app.api.websockets import register_events
    register_events(socketio)
    
    return app
