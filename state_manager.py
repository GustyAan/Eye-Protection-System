# state_manager.py
import datetime
import threading
from logger_db import DatabaseLogger

class StateManager:
    def __init__(self):
        self.logger = DatabaseLogger()
        
        # State variables
        self.face_detected = False
        self.screen_time = 0  # in seconds
        self.break_time = 0   # in seconds
        self.popup_active = False
        self.current_session_start = None
        self.last_detection_time = None
        self.monitoring_active = False  # Control monitoring state
        
        # Timers
        self.screen_timer = None
        self.break_timer = None
        self.minute_logger_timer = None
        
        # Callbacks
        self.on_popup_callback = None
        self.on_break_complete_callback = None
        
        # Debug counter
        self.debug_counter = 0
        
    def start_monitoring(self):
        """Start monitoring - called when entering user/dev mode"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self._reset_counters()  # Reset counters when starting fresh
            self._start_minute_logger()
            self.logger.log_activity("MONITORING_START", "Monitoring dimulai")
            print(" Monitoring started - counters reset")
            
    def stop_monitoring(self):
        """Stop monitoring - called when exiting user/dev mode"""
        if self.monitoring_active:
            self.monitoring_active = False
            self._stop_all_timers()
            self.logger.log_activity("MONITORING_STOP", "Monitoring dihentikan")
            print(" Monitoring stopped")
        
    def _reset_counters(self):
        """Reset all counters to initial state"""
        self.screen_time = 0
        self.break_time = 0
        self.popup_active = False
        self.face_detected = False
        self.current_session_start = None
        print("Counters reset to zero")
        
    def _start_minute_logger(self):
        """Start timer to log data every minute"""
        if self.monitoring_active:
            self._log_minute_data()
            self.minute_logger_timer = threading.Timer(60.0, self._start_minute_logger)
            self.minute_logger_timer.daemon = True
            self.minute_logger_timer.start()
            
    def _log_minute_data(self):
        """Log data for the current minute"""
        try:
            if self.monitoring_active:
                self.logger.log_minute_data(
                    datetime.datetime.now(),
                    self.face_detected,
                    self.screen_time,
                    self.break_time
                )
        except Exception as e:
            print(f"Error logging minute data: {e}")
            
    def update_face_detection(self, detected):
        """Update face detection state - only if monitoring is active"""
        if not self.monitoring_active:
            return False
            
        # Only update if detection status actually changes
        if detected != self.face_detected:
            old_state = self.face_detected
            self.face_detected = detected
            self.last_detection_time = datetime.datetime.now()
            
            if detected:
                # Face detected - start screen time, stop break time
                # Hanya mulai screen time jika belum mencapai batas 20 detik dan popup tidak aktif
                if self.screen_time < 20 and not self.popup_active:
                    self._start_screen_time()
                self._stop_break_time()
                self.break_time = 0  # Reset break time when face detected
                self.logger.log_activity("FACE_DETECTED", "Wajah terdeteksi")
                print("Face detected" + ("" if self.screen_time < 20 else " - Screen time already at limit, timer stopped"))
            else:
                # Face not detected - stop screen time, start break time
                self._stop_screen_time()
                # Hanya mulai break time jika popup aktif (sudah mencapai 20 detik)
                if self.popup_active:
                    self._start_break_time()
                self.logger.log_activity("FACE_NOT_DETECTED", "Wajah tidak terdeteksi")
                print("Face not detected" + (" - Starting break timer" if self.popup_active else " - No break needed"))
            
            return True
        return False
                
    def _start_screen_time(self):
        """Start or resume screen time counting"""
        if not self.monitoring_active or not self.face_detected:
            return
            
        # Jangan mulai jika sudah mencapai batas 20 detik atau popup aktif
        if self.screen_time >= 20 or self.popup_active:
            self._stop_screen_time()
            return
            
        # Cancel existing timer if any
        self._stop_screen_time()
            
        print("Starting screen timer...")
        self.screen_timer = threading.Timer(1.0, self._increment_screen_time)
        self.screen_timer.daemon = True
        self.screen_timer.start()
        
        if self.current_session_start is None:
            self.current_session_start = datetime.datetime.now()
            self.logger.log_activity("SESSION_START", "Sesi penggunaan dimulai")
            print("New session started")
            
    def _stop_screen_time(self):
        """Stop screen time counting"""
        if self.screen_timer and self.screen_timer.is_alive():
            self.screen_timer.cancel()
            self.screen_timer = None
            print("Screen timer stopped")
            
    def _increment_screen_time(self):
        """Increment screen time and check for limits"""
        # Hanya lanjut jika monitoring aktif, wajah terdeteksi, dan belum mencapai batas
        if self.monitoring_active and self.face_detected and self.screen_time < 20:
            self.screen_time += 1
            self.debug_counter += 1
            
            # Debug log every 5 seconds
            if self.debug_counter % 5 == 0:
                print(f"Screen time: {self.screen_time}s (Popup: {self.popup_active})")
            
            # Check if screen time limit reached
            if self.screen_time >= 20:
                print(f"Screen time limit reached: {self.screen_time}s - Stopping timer and showing popup")
                self._stop_screen_time()  # Hentikan timer screen time
                self._show_popup_warning()
                
            # Continue timer only jika masih dalam kondisi yang diperbolehkan
            elif self.monitoring_active and self.face_detected and self.screen_time < 20:
                self.screen_timer = threading.Timer(1.0, self._increment_screen_time)
                self.screen_timer.daemon = True
                self.screen_timer.start()
            else:
                self._stop_screen_time()
        else:
            self._stop_screen_time()
            
    def _show_popup_warning(self):
        """Show popup warning for excessive screen time"""
        if self.monitoring_active and not self.popup_active:
            self.popup_active = True
            self.logger.log_activity("POPUP_SHOWN", "Peringatan: Penggunaan layar melebihi 20 detik")
            print("Popup warning triggered - waiting for break...")
            
            # Hentikan screen time ketika popup aktif
            self._stop_screen_time()
            
            # Panggil callback dengan error handling
            if self.on_popup_callback:
                try:
                    self.on_popup_callback()
                    print("Popup callback executed successfully")
                except Exception as e:
                    print(f"Error in popup callback: {e}")
            else:
                print("No popup callback registered!")
            
    def _start_break_time(self):
        """Start break time counting"""
        # Hanya mulai break time jika monitoring aktif, wajah tidak terdeteksi, DAN popup aktif
        if not self.monitoring_active or self.face_detected or not self.popup_active:
            return
            
        # Cancel existing timer if any
        self._stop_break_time()
            
        print("Starting break timer...")
        self.break_timer = threading.Timer(1.0, self._increment_break_time)
        self.break_timer.daemon = True
        self.break_timer.start()
        
    def _stop_break_time(self):
        """Stop break time counting"""
        if self.break_timer and self.break_timer.is_alive():
            self.break_timer.cancel()
            self.break_timer = None
            print("Break timer stopped")
            
    def _increment_break_time(self):
        """Increment break time and check for completion"""
        # Hanya lanjut jika monitoring aktif, wajah tidak terdeteksi, popup aktif, dan belum mencapai 7 detik
        if (self.monitoring_active and not self.face_detected and 
            self.popup_active and self.break_time < 7):
            self.break_time += 1
            
            # Debug log
            if self.break_time % 3 == 0:
                print(f"Break time: {self.break_time}s (Popup: {self.popup_active})")
            
            # Check if break time requirement met
            if self.break_time >= 7:
                print(f"Break completed: {self.break_time}s - Resetting counters")
                self._complete_break()
                
            # Continue timer hanya jika masih dalam kondisi yang diperbolehkan
            elif (self.monitoring_active and not self.face_detected and 
                  self.popup_active and self.break_time < 7):
                self.break_timer = threading.Timer(1.0, self._increment_break_time)
                self.break_timer.daemon = True
                self.break_timer.start()
            else:
                self._stop_break_time()
        else:
            self._stop_break_time()
            
    def _complete_break(self):
        """Complete break and reset counters"""
        if self.monitoring_active:
            self.popup_active = False
            self.screen_time = 0
            self.break_time = 0
            self.debug_counter = 0
            
            # Hentikan semua timer
            self._stop_screen_time()
            self._stop_break_time()
            
            # End current session
            if self.current_session_start:
                session_end = datetime.datetime.now()
                duration = (session_end - self.current_session_start).seconds
                self.logger.log_usage_session(
                    self.current_session_start,
                    session_end,
                    duration,
                    True,  # face was detected
                    True,  # popup was shown
                    True   # break was taken
                )
                self.current_session_start = None
                
            self.logger.log_activity("BREAK_COMPLETE", "Istirahat 7 detik selesai")
            print(" Break completed - all counters reset and timers stopped")
            
            # Panggil callback dengan error handling
            if self.on_break_complete_callback:
                try:
                    self.on_break_complete_callback()
                    print("Break complete callback executed successfully")
                except Exception as e:
                    print(f" Error in break complete callback: {e}")
            else:
                print("No break complete callback registered!")
            
    def reset_counters(self):
        """Reset all counters manually"""
        if self.monitoring_active:
            self.screen_time = 0
            self.break_time = 0
            self.popup_active = False
            self.debug_counter = 0
            
            # Hentikan semua timer
            self._stop_screen_time()
            self._stop_break_time()
            
            if self.current_session_start:
                session_end = datetime.datetime.now()
                duration = (session_end - self.current_session_start).seconds
                self.logger.log_usage_session(
                    self.current_session_start,
                    session_end,
                    duration,
                    self.face_detected,
                    self.popup_active,
                    False  # break not taken
                )
                self.current_session_start = None
                
            self.logger.log_activity("MANUAL_RESET", "Pengguna mereset counter secara manual")
            print("Manual reset - counters cleared and timers stopped")
        
    def get_current_state(self):
        """Get current state as dictionary"""
        return {
            'face_detected': self.face_detected,
            'screen_time': self.screen_time,
            'break_time': self.break_time,
            'popup_active': self.popup_active,
            'session_active': self.current_session_start is not None,
            'monitoring_active': self.monitoring_active
        }
        
    def _stop_all_timers(self):
        """Stop all active timers"""
        self._stop_screen_time()
        self._stop_break_time()
        
    def cleanup(self):
        """Clean up timers and resources"""
        self.monitoring_active = False
        self._stop_all_timers()
        
        if self.minute_logger_timer and self.minute_logger_timer.is_alive():
            self.minute_logger_timer.cancel()
            
        # Log final session if active
        if self.current_session_start:
            session_end = datetime.datetime.now()
            duration = (session_end - self.current_session_start).seconds
            self.logger.log_usage_session(
                self.current_session_start,
                session_end,
                duration,
                self.face_detected,
                self.popup_active,
                self.break_time >= 7
            )