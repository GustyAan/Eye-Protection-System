# camera.py
import cv2
import threading
import time

class CameraManager:
    def __init__(self):
        self.camera = None
        self.is_running = False
        self.current_frame = None
        self.capture_thread = None
        self.on_frame_callback = None
        self.frame_lock = threading.Lock()
        
    def start_camera(self):
        """Start camera capture"""
        try:
            # Release existing camera if any
            if self.camera:
                self.camera.release()
                
            self.camera = cv2.VideoCapture(0)
            
            if not self.camera.isOpened():
                # Try camera index 1 if 0 fails
                self.camera = cv2.VideoCapture(1)
                if not self.camera.isOpened():
                    raise Exception("Cannot open any camera")
                    
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_running = True
            self.capture_thread = threading.Thread(target=self._capture_loop)
            self.capture_thread.daemon = True
            self.capture_thread.start()
            
            print("Camera started successfully")
            return True
            
        except Exception as e:
            print(f"Error starting camera: {e}")
            return False
            
    def _capture_loop(self):
        """Main capture loop"""
        while self.is_running:
            try:
                ret, frame = self.camera.read()
                
                if ret and frame is not None:
                    with self.frame_lock:
                        self.current_frame = frame
                    
                    if self.on_frame_callback:
                        self.on_frame_callback(frame)
                else:
                    print("Failed to read frame from camera")
                    
            except Exception as e:
                print(f"Error in capture loop: {e}")
                
            time.sleep(0.033)  # ~30 FPS
            
    def get_frame(self):
        """Get current frame with thread safety"""
        with self.frame_lock:
            return self.current_frame if self.current_frame is not None else None
            
    def stop_camera(self):
        """Stop camera capture"""
        self.is_running = False
        
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=2.0)
            
        if self.camera:
            self.camera.release()
            self.camera = None
            
        print("Camera stopped")
        
    def is_camera_available(self):
        """Check if camera is available and working"""
        if not self.camera:
            return False
            
        return self.camera.isOpened() and self.current_frame is not None

    def restart_camera(self):
        """Restart camera - useful when switching modes"""
        self.stop_camera()
        time.sleep(0.5)  # Brief pause
        return self.start_camera()