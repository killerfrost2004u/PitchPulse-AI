import time
from flask_socketio import SocketIO
from app.schemas.tracking import FrameData, Entity

def emit_mock_tracking_data(socketio: SocketIO):
    frame_id = 0
    while True:
        socketio.sleep(1.0) # Emit 1 FPS mock data
        frame_id += 1
        
        entity = Entity(id=1, label='player', team='team_a', position=(10.0 + (frame_id % 10), 20.0), speed=2.5)
        frame = FrameData(frame_id=frame_id, timestamp=time.time(), entities=[entity])
        
        socketio.emit('tracking_update', frame.model_dump())

def register_events(socketio: SocketIO):
    # Start the background task
    socketio.start_background_task(emit_mock_tracking_data, socketio)

    @socketio.on('connect')
    def handle_connect():
        print("Client connected to WebSocket")

    @socketio.on('disconnect')
    def handle_disconnect():
        print("Client disconnected from WebSocket")
