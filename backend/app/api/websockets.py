import time
from flask_socketio import SocketIO
from app.vision.tracker import VisionPipeline

# Global variable to hold the latest annotated frame for the MJPEG stream
_latest_frame_jpeg = b""

def get_latest_frame():
    global _latest_frame_jpeg
    return _latest_frame_jpeg

def emit_real_tracking_data(socketio: SocketIO):
    global _latest_frame_jpeg
    video_path = r"D:\Downloads\Test.mp4"
    pipeline = VisionPipeline("yolov8n.pt")
    
    while True:
        # Process the video frame-by-frame as a generator
        for frame_data, jpeg_bytes in pipeline.process_video(video_path):
            socketio.emit('tracking_update', frame_data.model_dump())
            
            if jpeg_bytes:
                _latest_frame_jpeg = jpeg_bytes
            
            # Sleep to yield control back to eventlet loop and cap emissions to 30 FPS
            # This prevents the CV loop from choking the WebSocket server
            socketio.sleep(1/30.0) 
            
        print("Video processing finished. Looping back to start...")
        socketio.sleep(2.0) # Give a small pause before restarting

def register_events(socketio: SocketIO):
    # Start the real vision background task
    socketio.start_background_task(emit_real_tracking_data, socketio)

    @socketio.on('connect')
    def handle_connect():
        print("Client connected to WebSocket")

    @socketio.on('disconnect')
    def handle_disconnect():
        print("Client disconnected from WebSocket")
