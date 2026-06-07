from flask import Blueprint, Response
import time
from app.api.websockets import get_latest_frame

video_bp = Blueprint('video', __name__)

@video_bp.route('/video_feed')
def video_feed():
    """
    Returns an MJPEG stream of the annotated OpenCV frames.
    """
    def generate():
        while True:
            frame = get_latest_frame()
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            # Throttle the HTTP stream to ~30 FPS
            time.sleep(1/30.0)
            
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
