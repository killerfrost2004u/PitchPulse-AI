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
            # Run YOLOv8 tracking, persist=True uses ByteTrack under the hood to keep IDs consistent
            results = self.model.track(frame, persist=True, verbose=False)
            
            entities = []
            
            if results and results[0].boxes:
                boxes = results[0].boxes
                
                # YOLO returns xyxy (top-left, bottom-right)
                for box in boxes:
                    # COCO dataset classes: 0=person, 32=sports ball
                    cls_id = int(box.cls[0].item())
                    
                    if cls_id not in [0, 32]:
                        continue
                    
                    label = "ball" if cls_id == 32 else "player"
                    
                    # Ensure the tracking algorithm assigned an ID
                    if box.id is None:
                        continue
                    track_id = int(box.id[0].item())
                    
                    # Calculate bottom-center for players (feet on ground mapping) 
                    # or center for ball
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    u = (x1 + x2) / 2.0
                    v = y2 if label == "player" else (y1 + y2) / 2.0
                    
                    # Apply homography transform to move from pixel space to 2D pitch space
                    x, y = mapper.transform(u, v)
                    
                    entities.append(Entity(
                        id=track_id,
                        label=label,
                        team=None, # TBD: Add team clustering logic based on shirt color
                        position=(x, y),
                        speed=0.0
                    ))
                    
            yield FrameData(
                frame_id=frame_id,
                timestamp=time.time(),
                entities=entities
            )
            
        cap.release()
