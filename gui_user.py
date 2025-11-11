# gui_user.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime
from config import LOGO_PATH
from PIL import Image, ImageTk
import os

class UserGUI:
    def __init__(self, root, state_manager, logger):
        self.root = root
        self.state_manager = state_manager
        self.logger = logger
        
        # Set up direct callbacks to this instance
        self.state_manager.on_popup_callback = self.show_popup_warning
        self.state_manager.on_break_complete_callback = self.show_break_complete
        
        # Start monitoring when entering user mode
        self.state_manager.start_monitoring()
        
        self.setup_ui()
        self.update_timer()
        
        print("📱 User GUI initialized with direct callbacks")
        
    def setup_ui(self):
        """Setup user interface"""
        self.root.title("Eye Protection System - User Mode")
        self.root.geometry("800x500")
        self.root.configure(bg='#f0f0f0')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Header frame with logo
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, text="Eye Protection System - Mode Pengguna", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Logo di kanan atas
        self.setup_logo(header_frame)
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status Real-time", padding="15")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        status_frame.columnconfigure(1, weight=1)
        
        # Detection status
        ttk.Label(status_frame, text="Status Wajah:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.face_status_var = tk.StringVar(value="Memulai deteksi...")
        self.face_status_label = ttk.Label(status_frame, textvariable=self.face_status_var, 
                     font=('Arial', 10, 'bold'))
        self.face_status_label.grid(row=0, column=1, sticky=tk.W)
        
        # Screen time
        ttk.Label(status_frame, text="Waktu Layar:", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.screen_time_var = tk.StringVar(value="0 detik")
        self.screen_time_label = ttk.Label(status_frame, textvariable=self.screen_time_var,
                     font=('Arial', 10, 'bold'))
        self.screen_time_label.grid(row=1, column=1, sticky=tk.W)
        
        # Break time
        ttk.Label(status_frame, text="Waktu Istirahat:", font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.break_time_var = tk.StringVar(value="0 detik")
        self.break_time_label = ttk.Label(status_frame, textvariable=self.break_time_var,
                     font=('Arial', 10, 'bold'))
        self.break_time_label.grid(row=2, column=1, sticky=tk.W)
        
        # Popup status
        ttk.Label(status_frame, text="Status Peringatan:", font=('Arial', 10)).grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
        self.popup_status_var = tk.StringVar(value="Tidak Aktif")
        self.popup_status_label = ttk.Label(status_frame, textvariable=self.popup_status_var,
                     font=('Arial', 10, 'bold'))
        self.popup_status_label.grid(row=3, column=1, sticky=tk.W)
        
        # Session status
        ttk.Label(status_frame, text="Sesi Aktif:", font=('Arial', 10)).grid(row=4, column=0, sticky=tk.W, padx=(0, 10))
        self.session_status_var = tk.StringVar(value="Tidak")
        self.session_status_label = ttk.Label(status_frame, textvariable=self.session_status_var,
                     font=('Arial', 10, 'bold'))
        self.session_status_label.grid(row=4, column=1, sticky=tk.W)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(0, 20))
        
        # Log activity button
        self.log_button = ttk.Button(button_frame, text="Lihat Log Aktivitas", 
                                    command=self.show_activity_log,
                                    style='Accent.TButton')
        self.log_button.grid(row=0, column=0, padx=(0, 15))
        
        # Reset counters button
        self.reset_button = ttk.Button(button_frame, text="Reset Counter", 
                                     command=self.reset_counters)
        self.reset_button.grid(row=0, column=1, padx=(0, 15))
        
        # Test popup button (untuk debugging)
        test_button = ttk.Button(button_frame, text="Test Popup", 
                               command=self.test_popup)
        test_button.grid(row=0, column=2, padx=(15, 0))
        
        # Information frame
        info_frame = ttk.LabelFrame(main_frame, text="Informasi Sistem", padding="10")
        info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Information text
        info_text = """Sistem akan memantau penggunaan layar Anda secara otomatis:
• Peringatan akan muncul setelah 20 detik penggunaan terus-menerus
• Istirahat 7 detik diperlukan untuk mereset timer
• Gunakan tombol 'Lihat Log Aktivitas' untuk melihat histori lengkap
• Tombol 'Reset Counter' untuk mengatur ulang manual
• Tombol 'Test Popup' untuk testing popup (development)"""
        
        info_label = ttk.Label(info_frame, text=info_text, font=('Arial', 9), justify=tk.LEFT)
        info_label.grid(row=0, column=0, sticky=tk.W)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
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
            
    def update_timer(self):
        """Update UI elements periodically"""
        state = self.state_manager.get_current_state()
        
        # Update status labels
        face_status = "Terdeteksi" if state['face_detected'] else "Tidak Terdeteksi"
        self.face_status_var.set(face_status)
        
        # Tampilkan screen time maksimal 20 detik
        screen_time_display = f"{min(state['screen_time'], 20)} detik"
        if state['screen_time'] >= 20:
            screen_time_display += " (MAKSIMAL)"
        self.screen_time_var.set(screen_time_display)
        
        # Tampilkan break time maksimal 7 detik
        break_time_display = f"{min(state['break_time'], 7)} detik"
        if state['break_time'] >= 7:
            break_time_display += " (CUKUP)"
        self.break_time_var.set(break_time_display)
        
        popup_status = "AKTIF - Istirahat diperlukan!" if state['popup_active'] else "Tidak Aktif"
        self.popup_status_var.set(popup_status)
        self.session_status_var.set("Ya" if state['session_active'] else "Tidak")
        
        # Update colors based on status
        face_color = 'green' if state['face_detected'] else 'red'
        popup_color = 'red' if state['popup_active'] else 'green'
        session_color = 'green' if state['session_active'] else 'red'
        
        self.face_status_label.configure(foreground=face_color)
        self.popup_status_label.configure(foreground=popup_color)
        self.session_status_label.configure(foreground=session_color)
        
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
            
        # Schedule next update
        self.root.after(1000, self.update_timer)
        
    def show_activity_log(self):
        """Show detailed activity log in new window"""
        try:
            activities = self.logger.get_activity_logs(100)
            
            # Create new window for detailed log
            log_window = tk.Toplevel(self.root)
            log_window.title("Log Aktivitas Detail - 10 Menit Terakhir")
            log_window.geometry("700x500")
            
            # Center the window
            log_window.transient(self.root)
            log_window.grab_set()
            
            # Header frame
            header_frame = ttk.Frame(log_window, padding="10")
            header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
            header_frame.columnconfigure(0, weight=1)
            
            title_label = ttk.Label(header_frame, text="Histori Aktivitas (10 Menit Terakhir)", 
                                   font=('Arial', 14, 'bold'))
            title_label.grid(row=0, column=0, sticky=tk.W)
            
            # Log text area
            log_frame = ttk.Frame(log_window, padding="10")
            log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            log_window.columnconfigure(0, weight=1)
            log_window.rowconfigure(1, weight=1)
            log_frame.columnconfigure(0, weight=1)
            log_frame.rowconfigure(0, weight=1)
            
            log_text = scrolledtext.ScrolledText(log_frame, width=80, height=20, font=('Arial', 9))
            log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            if not activities:
                log_text.insert(tk.END, "Tidak ada aktivitas yang tercatat.")
            else:
                # Filter activities for last 10 minutes
                ten_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=10)
                recent_activities = [act for act in activities if act['timestamp'] >= ten_minutes_ago]
                
                if not recent_activities:
                    log_text.insert(tk.END, "Tidak ada aktivitas dalam 10 menit terakhir.\n\n")
                else:
                    log_text.insert(tk.END, f"Aktivitas dalam 10 menit terakhir ({len(recent_activities)} entri):\n\n")
                    for activity in recent_activities:
                        timestamp = activity['timestamp'].strftime('%H:%M:%S')
                        log_line = f"[{timestamp}] {activity['type']}: {activity['description']}\n"
                        log_text.insert(tk.END, log_line)
                
                log_text.insert(tk.END, f"\n---\nTotal aktivitas tersimpan: {len(activities)} entri")
                    
            log_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat log: {e}")
            
    def reset_counters(self):
        """Reset counters manually"""
        self.state_manager.reset_counters()
        messagebox.showinfo("Counter Direset", "Counter waktu telah direset ke nol.")
        
    def test_popup(self):
        """Test popup functionality"""
        print(" Testing popup functionality...")
        self.show_popup_warning()
        
    def show_popup_warning(self):
        """Show popup warning - called from state manager"""
        print("📱 User Mode: Showing popup warning")
        # Gunakan after untuk memastikan popup muncul di thread UI yang benar
        self.root.after(0, self._show_popup_dialog)
        
    def _show_popup_dialog(self):
        """Actual popup dialog implementation"""
        try:
            messagebox.showwarning(
                "Peringatan Mata Lelah", 
                "Anda telah menggunakan layar selama 20 detik!\n\n"
                "Silakan istirahat dengan melihat kejauhan selama 7 detik.\n"
                "Timer akan direset otomatis setelah istirahat cukup."
            )
            print("✅ Popup warning shown successfully")
        except Exception as e:
            print(f"Error showing popup: {e}")
        
    def show_break_complete(self):
        """Show break complete message - called from state manager"""
        print("📱 User Mode: Showing break complete")
        # Gunakan after untuk memastikan popup muncul di thread UI yang benar
        self.root.after(0, self._show_break_complete_dialog)
        
    def _show_break_complete_dialog(self):
        """Actual break complete dialog implementation"""
        try:
            messagebox.showinfo(
                "Istirahat Selesai", 
                "Istirahat Anda telah cukup!\n\n"
                "Anda dapat melanjutkan aktivitas dengan layar."
            )
            print("Break complete popup shown successfully")
        except Exception as e:
            print(f"Error showing break complete popup: {e}")
    
    def on_close(self):
        """Handle window close - stop monitoring"""
        # Clear callbacks before closing
        self.state_manager.on_popup_callback = None
        self.state_manager.on_break_complete_callback = None
        self.state_manager.stop_monitoring()
        self.root.destroy()