# detector.py
import cv2
import numpy as np
from config import CASCADE_PATH
import os

class FaceDetector:
    def __init__(self):
        self.face_cascade = None
        self._load_cascade()
        
    def _load_cascade(self):
        """Load Haar cascade classifier"""
        try:
            # First try to load from models directory
            if os.path.exists(CASCADE_PATH):
                self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
                print(f"Loaded cascade from: {CASCADE_PATH}")
            else:
                # Fallback to OpenCV's built-in cascade
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
                print(f"Loaded cascade from: {cascade_path}")
                
            if self.face_cascade.empty():
                raise Exception("Failed to load cascade classifier")
                
            print("Cascade classifier loaded successfully")
        except Exception as e:
            print(f"Error loading cascade classifier: {e}")
            raise
            
    def detect_faces(self, frame):
        """Detect faces in the given frame"""
        if self.face_cascade is None or frame is None:
            return []
            
        try:
            # Convert to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces with optimized parameters
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(50, 50),  # Increased minimum size for better accuracy
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            return faces
            
        except Exception as e:
            print(f"Error in face detection: {e}")
            return []
            
    def draw_detection_boxes(self, frame, faces):
        """Draw detection boxes on the frame"""
        if frame is None:
            return frame
            
        try:
            for (x, y, w, h) in faces:
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Add label
                cv2.putText(frame, 'Wajah Terdeteksi', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                           
            return frame
        except Exception as e:
            print(f"Error drawing detection boxes: {e}")
            return frame
            
    def get_detection_status(self, faces):
        """Get detection status based on number of faces detected"""
        return len(faces) > 0