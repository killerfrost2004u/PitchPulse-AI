import time
from flask_socketio import SocketIO
from app.vision.tracker import VisionPipeline

def emit_real_tracking_data(socketio: SocketIO):
    video_path = r"D:\Downloads\Test.mp4"
    pipeline = VisionPipeline("yolov8n.pt")
    
    # Process the video frame-by-frame as a generator
    for frame_data in pipeline.process_video(video_path):
        socketio.emit('tracking_update', frame_data.model_dump())
        
        # Sleep to yield control back to eventlet loop and cap emissions to 30 FPS
        # This prevents the CV loop from choking the WebSocket server
        socketio.sleep(1/30.0) 
        
    print("Video processing finished.")

def register_events(socketio: SocketIO):
    # Start the real vision background task
    socketio.start_background_task(emit_real_tracking_data, socketio)

    @socketio.on('connect')
    def handle_connect():
        print("Client connected to WebSocket")

    @socketio.on('disconnect')
    def handle_disconnect():
        print("Client disconnected from WebSocket")
