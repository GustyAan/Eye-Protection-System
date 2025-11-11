# main.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os
import threading
import time
import cv2

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import DEV_PASSWORD
from state_manager import StateManager
from logger_db import DatabaseLogger
from camera import CameraManager
from detector import FaceDetector
from gui_user import UserGUI
from gui_dev import DeveloperGUI

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        
        # Initialize components
        self.logger = DatabaseLogger()
        self.state_manager = StateManager()
        self.camera_manager = CameraManager()
        self.face_detector = FaceDetector()
        
        # Set up callbacks
        self.state_manager.on_popup_callback = self.show_popup_warning
        self.state_manager.on_break_complete_callback = self.show_break_complete
        
        # Start camera but DON'T start monitoring yet
        self.camera_manager.start_camera()
        
        # Track active windows
        self.active_user_window = None
        self.active_dev_window = None
        
        # Face detection control
        self.face_detection_active = False
        self.face_detection_thread = None
        
        # Start universal face detection
        self.start_universal_face_detection()
        
    def setup_main_window(self):
        """Setup main menu window"""
        self.root.title("Eye Protection System")
        self.root.geometry("500x350")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)
        
        # Center window
        self.center_window(500, 350)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header frame with logo
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, text="Eye Protection System", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Logo di kanan atas
        self.setup_logo(header_frame)
        
        # Content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        
        # Subtitle
        subtitle_label = ttk.Label(content_frame, text="Sistem Proteksi Mata Pengguna", 
                                  font=('Arial', 12))
        subtitle_label.grid(row=0, column=0, pady=(0, 40))
        
        # User mode button
        user_btn = ttk.Button(content_frame, text="Mode Pengguna", 
                             command=self.start_user_mode,
                             style='Accent.TButton')
        user_btn.grid(row=1, column=0, pady=(0, 15), sticky=(tk.W, tk.E))
        
        # Developer mode button
        dev_btn = ttk.Button(content_frame, text="Mode Developer", 
                            command=self.authenticate_developer)
        dev_btn.grid(row=2, column=0, pady=(0, 15), sticky=(tk.W, tk.E))
        
        # Exit button
        exit_btn = ttk.Button(content_frame, text="Keluar", 
                             command=self.cleanup_and_exit)
        exit_btn.grid(row=3, column=0, sticky=(tk.W, tk.E))
    
    def setup_logo(self, parent):
        """Setup PENS logo di kanan atas"""
        try:
            from config import LOGO_PATH
            from PIL import Image, ImageTk
            import os
            
            if os.path.exists(LOGO_PATH):
                image = Image.open(LOGO_PATH)
                image = image.resize((60, 60), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(image)
                
                logo_label = ttk.Label(parent, image=self.logo_image)
                logo_label.grid(row=0, column=1, sticky=tk.NE)
            else:
                # Create placeholder if logo doesn't exist
                logo_label = ttk.Label(parent, text="LOGO PENS", 
                                     font=('Arial', 8, 'italic'), 
                                     foreground='gray')
                logo_label.grid(row=0, column=1, sticky=tk.NE)
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_label = ttk.Label(parent, text="LOGO PENS", 
                                 font=('Arial', 8, 'italic'), 
                                 foreground='gray')
            logo_label.grid(row=0, column=1, sticky=tk.NE)
        
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def start_universal_face_detection(self):
        """Start universal face detection that works for both modes"""
        self.face_detection_active = True
        self.face_detection_thread = threading.Thread(target=self._face_detection_loop)
        self.face_detection_thread.daemon = True
        self.face_detection_thread.start()
        print("🔍 Universal face detection started")
        
    def _face_detection_loop(self):
        """Universal face detection loop for both user and developer modes"""
        while self.face_detection_active:
            try:
                # Only process if monitoring is active (in user or developer mode)
                if self.state_manager.monitoring_active:
                    frame = self.camera_manager.get_frame()
                    
                    if frame is not None:
                        faces = self.face_detector.detect_faces(frame)
                        face_detected = len(faces) > 0
                        
                        # Update state manager
                        self.state_manager.update_face_detection(face_detected)
                        
                        # Debug log occasionally
                        if hasattr(self, 'detection_counter'):
                            self.detection_counter += 1
                            if self.detection_counter % 30 == 0:  # Log every 30 detections
                                status = "terdeteksi" if face_detected else "tidak terdeteksi"
                                print(f"🔍 Face detection: {status} ({len(faces)} faces)")
                        else:
                            self.detection_counter = 0
                    else:
                        print(" No frame available for face detection")
                else:
                    # Monitoring not active, sleep longer to save resources
                    time.sleep(2)
                    
            except Exception as e:
                print(f"Face detection error: {e}")
                
            time.sleep(0.5)  # Check every 0.5 seconds
            
    def start_user_mode(self):
        """Start user mode interface"""
        print("Starting User Mode...")
        
        # Stop any existing monitoring first
        self.state_manager.stop_monitoring()
        
        # Close any existing windows
        if self.active_dev_window:
            self.active_dev_window.destroy()
            self.active_dev_window = None
            
        # Ensure camera is running
        if not self.camera_manager.is_camera_available():
            success = self.camera_manager.restart_camera()
            if not success:
                messagebox.showerror("Error", "Tidak dapat mengakses kamera")
                return
        
        self.root.withdraw()  # Hide main window
        
        user_window = tk.Toplevel(self.root)
        user_window.title("Eye Protection System - User Mode")
        user_window.geometry("800x500")
        self.center_window_on_screen(user_window, 800, 500)
        
        # Create user GUI and store reference
        user_gui = UserGUI(user_window, self.state_manager, self.logger)
        self.active_user_window = user_window
        
        # Handle window close
        user_window.protocol("WM_DELETE_WINDOW", lambda: self.on_user_close(user_window))
        
        print("User Mode started successfully")
        
    def authenticate_developer(self):
        """Authenticate developer mode"""
        password = simpledialog.askstring(
            "Autentikasi Developer", 
            "Masukkan password developer:", 
            show='*'
        )
        
        if password == DEV_PASSWORD:
            self.start_developer_mode()
        elif password is not None:  # User pressed cancel returns None
            messagebox.showerror("Error", "Password salah!")
            
    def start_developer_mode(self):
        """Start developer mode interface"""
        print("Starting Developer Mode...")
        
        # Stop any existing monitoring first
        self.state_manager.stop_monitoring()
        
        # Close any existing windows
        if self.active_user_window:
            self.active_user_window.destroy()
            self.active_user_window = None
            
        # Ensure camera is running
        if not self.camera_manager.is_camera_available():
            success = self.camera_manager.restart_camera()
            if not success:
                messagebox.showerror("Error", "Tidak dapat mengakses kamera")
                return
            
        self.root.withdraw()  # Hide main window
        
        dev_window = tk.Toplevel(self.root)
        dev_window.title("Eye Protection System - Developer Mode")
        dev_window.geometry("1100x750")
        self.center_window_on_screen(dev_window, 1100, 750)
        
        # Create developer GUI and store reference
        dev_gui = DeveloperGUI(dev_window, self.state_manager, self.logger, 
                             self.camera_manager, self.face_detector)
        self.active_dev_window = dev_window
        
        # Handle window close
        dev_window.protocol("WM_DELETE_WINDOW", lambda: self.on_dev_close(dev_window))
        
        print("Developer Mode started successfully")
        
    def center_window_on_screen(self, window, width, height):
        """Center a window on screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
        
    def on_user_close(self, user_window):
        """Handle user window close"""
        user_window.destroy()
        self.active_user_window = None
        self.state_manager.stop_monitoring()  # Ensure monitoring stops
        self.root.deiconify()  # Show main window again
        print("User mode closed")
        
    def on_dev_close(self, dev_window):
        """Handle developer window close"""
        dev_window.destroy()
        self.active_dev_window = None
        self.state_manager.stop_monitoring()  # Ensure monitoring stops
        self.root.deiconify()  # Show main window again
        print("Developer mode closed")
        
    def show_popup_warning(self):
        """Show popup warning for excessive screen time"""
        print("Popup warning callback triggered")
        
        # Show warning based on which window is active
        if self.active_user_window and self.active_user_window.winfo_exists():
            print("📱 Showing popup in User Mode")
            # Find the user GUI instance and call its method
            for widget in self.active_user_window.winfo_children():
                if hasattr(widget, 'show_popup_warning'):
                    widget.show_popup_warning()
                    return
        elif self.active_dev_window and self.active_dev_window.winfo_exists():
            print("Showing popup in Developer Mode")
            # For developer mode, show simple messagebox
            messagebox.showwarning(
                "Peringatan Mata Lelah", 
                "Pengguna telah menggunakan layar selama 20 detik!\n\n"
                "Sistem menunggu istirahat 7 detik..."
            )
        else:
            print("No active window found for popup")
        
    def show_break_complete(self):
        """Show break complete message"""
        print("Break complete callback triggered")
        
        # Show message based on which window is active
        if self.active_user_window and self.active_user_window.winfo_exists():
            print("📱 Showing break complete in User Mode")
            # Find the user GUI instance and call its method
            for widget in self.active_user_window.winfo_children():
                if hasattr(widget, 'show_break_complete'):
                    widget.show_break_complete()
                    return
        elif self.active_dev_window and self.active_dev_window.winfo_exists():
            print("Showing break complete in Developer Mode")
            # For developer mode, show simple messagebox
            messagebox.showinfo(
                "Istirahat Selesai", 
                "Istirahat telah cukup!\nTimer direset otomatis."
            )
        else:
            print("No active window found for break complete")
        
    def cleanup_and_exit(self):
        """Clean up resources and exit"""
        try:
            print("Cleaning up resources...")
            self.face_detection_active = False
            self.state_manager.stop_monitoring()
            self.state_manager.cleanup()
            self.camera_manager.stop_camera()
            self.logger.log_activity("SYSTEM", "Aplikasi ditutup")
            
            # Close any active windows
            if self.active_user_window:
                self.active_user_window.destroy()
            if self.active_dev_window:
                self.active_dev_window.destroy()
                
            print("Cleanup completed")
                
        except Exception as e:
            print(f"Error during cleanup: {e}")
            
        self.root.quit()
        self.root.destroy()
        
    def run(self):
        """Start the application"""
        try:
            self.logger.log_activity("SYSTEM", "Aplikasi dimulai")
            print("Application starting...")
            self.root.mainloop()
        except KeyboardInterrupt:
            print(" Keyboard interrupt received")
            self.cleanup_and_exit()
        except Exception as e:
            print(f"Application error: {e}")
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
            self.cleanup_and_exit()

if __name__ == "__main__":
    # Set up error handling
    try:
        app = MainApplication()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        input("Press Enter to exit...")