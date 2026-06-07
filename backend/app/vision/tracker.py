import cv2
import time
from ultralytics import YOLO
from app.schemas.tracking import FrameData, Entity
from app.vision.homography import PitchMapper

class VisionPipeline:
    def __init__(self, model_path="yolov8n.pt"):
        # Load the nano model, specifically chosen to fit within the 2GB VRAM constraint
        print(f"Loading vision model: {model_path}")
        self.model = YOLO(model_path)
    
    def process_video(self, video_path: str):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error opening video file: {video_path}")
            return
            
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        mapper = PitchMapper(frame_width, frame_height)
        frame_id = 0
        
        print("Starting video processing loop...")
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("End of video stream or failed to read frame.")
                break
            
            frame_id += 1
            # Run YOLOv8 tracking with tuned parameters for tiny sports players
            # imgsz=1280 forces high-res analysis, conf=0.15 catches distant players
            # tracker="botsort.yaml" or "bytetrack.yaml" reduces ID flashing
            results = self.model.track(
                frame, 
                persist=True, 
                verbose=False,
                imgsz=1280,
                conf=0.15,
                iou=0.45,
                tracker="bytetrack.yaml"
            )
            
            entities = []
            
            if results and results[0].boxes:
                boxes = results[0].boxes
                
                for box in boxes:
                    cls_id = int(box.cls[0].item())
                    if cls_id not in [0, 32]:
                        continue
                    
                    label = "ball" if cls_id == 32 else "player"
                    
                    if box.id is None:
                        continue
                    track_id = int(box.id[0].item())
                    
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    u = (x1 + x2) / 2.0
                    v = y2 if label == "player" else (y1 + y2) / 2.0
                    
                    x, y = mapper.transform(u, v)
                    
                    entities.append(Entity(
                        id=track_id,
                        label=label,
                        team=None,
                        position=(x, y),
                        speed=0.0
                    ))

                    # Draw bounding box and ID on the OpenCV frame
                    color = (0, 255, 255) if label == "player" else (255, 255, 255)
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    cv2.putText(frame, f"{label} {track_id}", (int(x1), int(y1)-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
            frame_data = FrameData(
                frame_id=frame_id,
                timestamp=time.time(),
                entities=entities
            )

            # Encode the annotated frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            jpeg_bytes = buffer.tobytes() if ret else None
            
            yield frame_data, jpeg_bytes
            
        cap.release()
