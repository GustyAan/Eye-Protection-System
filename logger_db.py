# logger_db.py
import sqlite3
import datetime
from config import DB_PATH, DATA_DIR
import os

class DatabaseLogger:
    def __init__(self):
        self._create_database()
        
    def _create_database(self):
        """Create database and tables if they don't exist"""
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create usage history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration_seconds INTEGER,
                face_detected INTEGER,
                popup_shown INTEGER,
                break_taken INTEGER
            )
        ''')
        
        # Create minute logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS minute_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                face_detected INTEGER,
                screen_time INTEGER,
                break_time INTEGER
            )
        ''')
        
        # Create activity logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def log_usage_session(self, start_time, end_time, duration, face_detected, popup_shown, break_taken):
        """Log a complete usage session"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO usage_history 
            (start_time, end_time, duration_seconds, face_detected, popup_shown, break_taken)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (start_time.isoformat(), end_time.isoformat() if end_time else None, 
              duration, face_detected, popup_shown, break_taken))
        
        conn.commit()
        conn.close()
        
    def log_minute_data(self, timestamp, face_detected, screen_time, break_time):
        """Log data for each minute"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO minute_logs 
            (timestamp, face_detected, screen_time, break_time)
            VALUES (?, ?, ?, ?)
        ''', (timestamp.isoformat(), face_detected, screen_time, break_time))
        
        conn.commit()
        conn.close()
        
    def log_activity(self, activity_type, description):
        """Log general activities"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activity_logs 
            (timestamp, activity_type, description)
            VALUES (?, ?, ?)
        ''', (datetime.datetime.now().isoformat(), activity_type, description))
        
        conn.commit()
        conn.close()
        
    def get_recent_minute_logs(self, minutes=10):
        """Get recent minute logs for graphing"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, face_detected, screen_time, break_time 
            FROM minute_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (minutes,))
        
        results = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        logs = []
        for row in results:
            logs.append({
                'timestamp': datetime.datetime.fromisoformat(row[0]),
                'face_detected': row[1],
                'screen_time': row[2],
                'break_time': row[3]
            })
            
        return logs[::-1]  # Reverse to get chronological order
        
    def get_usage_stats(self, hours=24):
        """Get usage statistics for specified hours"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        time_threshold = (datetime.datetime.now() - datetime.timedelta(hours=hours)).isoformat()
        
        cursor.execute('''
            SELECT 
                SUM(duration_seconds) as total_screen_time,
                SUM(break_taken) as total_breaks,
                COUNT(*) as total_sessions
            FROM usage_history 
            WHERE start_time > ?
        ''', (time_threshold,))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total_screen_time': result[0] or 0,
            'total_breaks': result[1] or 0,
            'total_sessions': result[2] or 0
        }
        
    def get_activity_logs(self, limit=50):
        """Get recent activity logs"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, activity_type, description 
            FROM activity_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        activities = []
        for row in results:
            activities.append({
                'timestamp': datetime.datetime.fromisoformat(row[0]),
                'type': row[1],
                'description': row[2]
            })
            
        return activities