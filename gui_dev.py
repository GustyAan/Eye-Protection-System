# gui_dev.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import cv2
from PIL import Image, ImageTk
import datetime
from config import LOGO_PATH
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class DeveloperGUI:
    def __init__(self, root, state_manager, logger, camera_manager, face_detector):
        self.root = root
        self.state_manager = state_manager
        self.logger = logger
        self.camera_manager = camera_manager
        self.face_detector = face_detector
        
        # Start monitoring when entering developer mode
        self.state_manager.start_monitoring()
        
        self.setup_ui()
        self.start_camera_feed()
        self.update_timer()
        
    def setup_ui(self):
        """Setup developer interface"""
        self.root.title("Eye Protection System - Developer Mode")
        self.root.geometry("1100x750")
        self.root.configure(bg='#f0f0f0')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header frame with logo
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, text="Eye Protection System - Mode Developer", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Logo di kanan atas
        self.setup_logo(header_frame)
        
        # Left frame - Camera and status
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        # Camera frame
        camera_frame = ttk.LabelFrame(left_frame, text="Kamera Live Feed - Deteksi Wajah", padding="5")
        camera_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        camera_frame.columnconfigure(0, weight=1)
        camera_frame.rowconfigure(0, weight=1)
        
        self.camera_label = ttk.Label(camera_frame, text="Menginisialisasi kamera...", font=('Arial', 9))
        self.camera_label.grid(row=0, column=0)
        
        # Status frame
        status_frame = ttk.LabelFrame(left_frame, text="Status Sistem Real-time", padding="10")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(1, weight=1)
        
        # Status labels
        ttk.Label(status_frame, text="Deteksi Wajah:", font=('Arial', 9)).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.face_status_var = tk.StringVar(value="Tidak Terdeteksi")
        self.face_status_label = ttk.Label(status_frame, textvariable=self.face_status_var, 
                     font=('Arial', 9, 'bold'))
        self.face_status_label.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(status_frame, text="Waktu Layar:", font=('Arial', 9)).grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.screen_time_var = tk.StringVar(value="0 detik")
        self.screen_time_label = ttk.Label(status_frame, textvariable=self.screen_time_var,
                     font=('Arial', 9, 'bold'))
        self.screen_time_label.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(status_frame, text="Waktu Istirahat:", font=('Arial', 9)).grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.break_time_var = tk.StringVar(value="0 detik")
        self.break_time_label = ttk.Label(status_frame, textvariable=self.break_time_var,
                     font=('Arial', 9, 'bold'))
        self.break_time_label.grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(status_frame, text="Status Popup:", font=('Arial', 9)).grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
        self.popup_status_var = tk.StringVar(value="Tidak Aktif")
        self.popup_status_label = ttk.Label(status_frame, textvariable=self.popup_status_var,
                     font=('Arial', 9, 'bold'))
        self.popup_status_label.grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(status_frame, text="Sesi Aktif:", font=('Arial', 9)).grid(row=4, column=0, sticky=tk.W, padx=(0, 10))
        self.session_status_var = tk.StringVar(value="Tidak")
        self.session_status_label = ttk.Label(status_frame, textvariable=self.session_status_var,
                     font=('Arial', 9, 'bold'))
        self.session_status_label.grid(row=4, column=1, sticky=tk.W)
        
        ttk.Label(status_frame, text="Monitoring:", font=('Arial', 9)).grid(row=5, column=0, sticky=tk.W, padx=(0, 10))
        self.monitoring_status_var = tk.StringVar(value="Aktif")
        self.monitoring_status_label = ttk.Label(status_frame, textvariable=self.monitoring_status_var,
                     font=('Arial', 9, 'bold'))
        self.monitoring_status_label.grid(row=5, column=1, sticky=tk.W)
        
        # Right frame - Graph and logs
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Graph frame
        graph_frame = ttk.LabelFrame(right_frame, text="Grafik Penggunaan (10 Menit Terakhir)", 
                                    padding="5")
        graph_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(0, weight=1)
        
        # Create graph
        self.setup_graph(graph_frame)
        
        # Logs frame
        logs_frame = ttk.LabelFrame(right_frame, text="Log Aktivitas Sistem", padding="5")
        logs_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(1, weight=1)
        
        # Log controls frame
        log_controls_frame = ttk.Frame(logs_frame)
        log_controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Control buttons
        self.reset_btn = ttk.Button(log_controls_frame, text="Reset Counter", 
                                   command=self.state_manager.reset_counters)
        self.reset_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.refresh_logs_btn = ttk.Button(log_controls_frame, text="Refresh Logs", 
                                         command=self.refresh_logs)
        self.refresh_logs_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.clear_logs_btn = ttk.Button(log_controls_frame, text="Clear Display", 
                                       command=self.clear_logs_display)
        self.clear_logs_btn.grid(row=0, column=2)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(logs_frame, width=60, height=15, font=('Arial', 8))
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Configure weights for proper resizing
        left_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        
    def setup_logo(self, parent):
        """Setup PENS logo di kanan atas"""
        try:
            if os.path.exists(LOGO_PATH):
                image = Image.open(LOGO_PATH)
                image = image.resize((80, 80), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(image)
                
                logo_label = ttk.Label(parent, image=self.logo_image)
                logo_label.grid(row=0, column=1, sticky=tk.NE)
            else:
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
            
    def setup_graph(self, parent):
        """Setup matplotlib graph"""
        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.update_graph()
        
    def update_graph(self):
        """Update the graph with recent data"""
        try:
            logs = self.logger.get_recent_minute_logs(10)
            
            if not logs:
                # Show empty graph
                self.ax.clear()
                self.ax.text(0.5, 0.5, 'Tidak ada data monitoring', ha='center', va='center', 
                            transform=self.ax.transAxes, fontsize=10)
                self.ax.set_title('Data Penggunaan Per Menit')
                self.canvas.draw()
                return
            
            timestamps = [log['timestamp'].strftime('%H:%M') for log in logs]
            screen_times = [log['screen_time'] for log in logs]
            break_times = [log['break_time'] for log in logs]
            
            self.ax.clear()
            
            x = range(len(timestamps))
            width = 0.35
            
            self.ax.bar([i - width/2 for i in x], screen_times, width, label='Waktu Layar', color='red', alpha=0.7)
            self.ax.bar([i + width/2 for i in x], break_times, width, label='Waktu Istirahat', color='green', alpha=0.7)
            
            self.ax.set_xlabel('Waktu')
            self.ax.set_ylabel('Detik')
            self.ax.set_title('Data Penggunaan Per Menit (10 Menit Terakhir)')
            self.ax.set_xticks(x)
            self.ax.set_xticklabels(timestamps, rotation=45)
            self.ax.legend()
            self.ax.grid(True, alpha=0.3)
            
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error updating graph: {e}")
                
    def start_camera_feed(self):
        """Start updating camera feed"""
        if self.camera_manager.is_camera_available():
            self.update_camera_feed()
        else:
            self.camera_label.configure(text="Kamera tidak tersedia")
            
    def update_camera_feed(self):
        """Update camera feed with face detection"""
        frame = self.camera_manager.get_frame()
        
        if frame is not None:
            # Detect faces
            faces = self.face_detector.detect_faces(frame)
            
            # Update state manager (only if monitoring is active)
            self.state_manager.update_face_detection(len(faces) > 0)
            
            # Draw detection boxes
            frame_with_boxes = self.face_detector.draw_detection_boxes(frame.copy(), faces)
            
            # Convert to PhotoImage
            rgb_frame = cv2.cvtColor(frame_with_boxes, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image=img)
            
            self.camera_label.configure(image=photo)
            self.camera_label.image = photo
            
        # Schedule next update
        self.root.after(50, self.update_camera_feed)
        
    def update_timer(self):
        """Update UI elements periodically"""
        state = self.state_manager.get_current_state()
        
        # Update status labels
        self.face_status_var.set("TERDETEKSI" if state['face_detected'] else "TIDAK TERDETEKSI")
        
        # Tampilkan screen time maksimal 20 detik
        screen_time_display = f"{min(state['screen_time'], 20)} detik"
        if state['screen_time'] >= 20:
            screen_time_display += " (MAX)"
        self.screen_time_var.set(screen_time_display)
        
        # Tampilkan break time maksimal 7 detik
        break_time_display = f"{min(state['break_time'], 7)} detik"
        if state['break_time'] >= 7:
            break_time_display += " (DONE)"
        self.break_time_var.set(break_time_display)
        
        self.popup_status_var.set("AKTIF" if state['popup_active'] else "TIDAK AKTIF")
        self.session_status_var.set("YA" if state['session_active'] else "TIDAK")
        self.monitoring_status_var.set("AKTIF" if state['monitoring_active'] else "NON-AKTIF")
        
        # Update colors
        face_color = 'green' if state['face_detected'] else 'red'
        popup_color = 'red' if state['popup_active'] else 'green'
        session_color = 'green' if state['session_active'] else 'red'
        monitoring_color = 'green' if state['monitoring_active'] else 'red'
        
        self.face_status_label.configure(foreground=face_color)
        self.popup_status_label.configure(foreground=popup_color)
        self.session_status_label.configure(foreground=session_color)
        self.monitoring_status_label.configure(foreground=monitoring_color)
        
        # Update screen time color based on warning level
        if state['screen_time'] >= 15 and state['screen_time'] < 20:
            self.screen_time_label.configure(foreground='orange')
        elif state['screen_time'] >= 20:
            self.screen_time_label.configure(foreground='red')
        else:
            self.screen_time_label.configure(foreground='black')
            
        # Update break time color
        if state['break_time'] >= 7:
            self.break_time_label.configure(foreground='green')
        elif state['break_time'] > 0:
            self.break_time_label.configure(foreground='blue')
        else:
            self.break_time_label.configure(foreground='black')
        
        # Update graph every 30 seconds
        if hasattr(self, 'graph_update_count'):
            self.graph_update_count += 1
            if self.graph_update_count >= 30:  # Update graph every 30 seconds
                self.update_graph()
                self.graph_update_count = 0
        else:
            self.graph_update_count = 0
            
        # Update logs every 10 seconds
        if hasattr(self, 'log_update_count'):
            self.log_update_count += 1
            if self.log_update_count >= 10:  # Update logs every 10 seconds
                self.refresh_logs()
                self.log_update_count = 0
        else:
            self.log_update_count = 0
            
        # Schedule next update
        self.root.after(1000, self.update_timer)
        
    def refresh_logs(self):
        """Refresh activity logs"""
        try:
            activities = self.logger.get_activity_logs(50)  # Last 50 activities
            
            self.log_text.delete(1.0, tk.END)
            
            if not activities:
                self.log_text.insert(tk.END, "Tidak ada aktivitas yang tercatat.\n")
                return
                
            # Show monitoring activities only
            monitoring_activities = [act for act in activities if act['type'] in [
                'MONITORING_START', 'MONITORING_STOP', 'FACE_DETECTED', 'FACE_NOT_DETECTED',
                'POPUP_SHOWN', 'BREAK_COMPLETE', 'SESSION_START', 'MANUAL_RESET'
            ]]
            
            if not monitoring_activities:
                self.log_text.insert(tk.END, "Tidak ada aktivitas monitoring.\n")
                return
                
            for activity in monitoring_activities:
                timestamp = activity['timestamp'].strftime('%H:%M:%S')
                log_line = f"[{timestamp}] {activity['type']}: {activity['description']}\n"
                self.log_text.insert(tk.END, log_line)
                
        except Exception as e:
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, f"Error loading logs: {e}")
    
    def clear_logs_display(self):
        """Clear the logs display (not the actual database)"""
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Log display cleared. Data tetap tersimpan di database.\n")
        
    def on_close(self):
        """Handle window close - stop monitoring before closing"""
        self.state_manager.stop_monitoring()
        self.root.destroy()