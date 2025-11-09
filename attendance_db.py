import sqlite3
from datetime import datetime
import os

class AttendanceDatabase:
    """Central database for managing attendance records"""
    
    def __init__(self, db_name='attendance.db'):
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        """Create attendance table if it doesn't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_attendance(self, name, date, time):
        """Add a new attendance record"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO attendance (name, date, time)
            VALUES (?, ?, ?)
        ''', (name, date, time))
        
        conn.commit()
        conn.close()
    
    def get_all_records(self):
        """Get all attendance records"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, date, time, timestamp
            FROM attendance
            ORDER BY date DESC, time DESC
        ''')
        
        records = cursor.fetchall()
        conn.close()
        
        return records
    
    def get_records_by_name(self, name):
        """Get attendance records for a specific person"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, date, time, timestamp
            FROM attendance
            WHERE name LIKE ?
            ORDER BY date DESC, time DESC
        ''', (f'%{name}%',))
        
        records = cursor.fetchall()
        conn.close()
        
        return records
    
    def get_records_by_date(self, date):
        """Get attendance records for a specific date"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, date, time, timestamp
            FROM attendance
            WHERE date = ?
            ORDER BY time DESC
        ''', (date,))
        
        records = cursor.fetchall()
        conn.close()
        
        return records
    
    def get_unique_dates(self):
        """Get all unique dates"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT date
            FROM attendance
            ORDER BY date DESC
        ''')
        
        dates = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return dates
    
    def get_unique_names(self):
        """Get all unique names"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT name
            FROM attendance
            ORDER BY name
        ''')
        
        names = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return names
    
    def get_statistics(self):
        """Get attendance statistics"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Total records
        cursor.execute('SELECT COUNT(*) FROM attendance')
        total_records = cursor.fetchone()[0]
        
        # Unique people
        cursor.execute('SELECT COUNT(DISTINCT name) FROM attendance')
        unique_people = cursor.fetchone()[0]
        
        # Unique dates
        cursor.execute('SELECT COUNT(DISTINCT date) FROM attendance')
        unique_dates = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_records': total_records,
            'unique_people': unique_people,
            'unique_dates': unique_dates
        }
    
    def delete_record(self, record_id):
        """Delete a specific attendance record"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM attendance WHERE id = ?', (record_id,))
        
        conn.commit()
        conn.close()
    
    def clear_all_records(self):
        """Clear all attendance records (use with caution!)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM attendance')
        
        conn.commit()
        conn.close()

