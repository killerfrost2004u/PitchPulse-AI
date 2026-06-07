import numpy as np

class PitchMapper:
    def __init__(self, frame_width: int, frame_height: int):
        # MVP: Naive scaling of the frame to a 100x100 radar grid (percentage-based)
        # In a full implementation, we'd take 4 reference points from the pitch 
        # and calculate a true `cv2.getPerspectiveTransform` matrix.
        self.frame_width = frame_width
        self.frame_height = frame_height
        
    def transform(self, u: float, v: float) -> tuple[float, float]:
        """
        Maps the pixel coordinates (u, v) to the 2D pitch coordinates (x, y).
        MVP: Basic scaling factor. u maps to x, v maps to y.
        """
        # Clamp to bounds to ensure coordinates don't fall off the radar
        u = max(0, min(u, self.frame_width))
        v = max(0, min(v, self.frame_height))
        
        # Scale to 0-100 grid for the UI radar percentage placement
        x = (u / self.frame_width) * 100.0
        y = (v / self.frame_height) * 100.0
        
        return (x, y)
