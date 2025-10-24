
# 2. Database Handler (database.py)
database_py = '''import sqlite3
import os

class Database:
    def __init__(self, db_name='studyflow.db'):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_name = os.path.join(BASE_DIR, db_name)
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                coins INTEGER DEFAULT 0,
                theme TEXT DEFAULT 'light',
                spotify_connected INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                total_duration INTEGER NOT NULL,
                breaks TEXT NOT NULL,
                net_study_time INTEGER NOT NULL,
                improvements TEXT,
                mistakes TEXT,
                ai_rating INTEGER NOT NULL,
                ai_suggestions TEXT,
                coins_earned INTEGER NOT NULL,
                subject TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                creator TEXT NOT NULL,
                description TEXT,
                max_participants INTEGER DEFAULT 6,
                participants TEXT DEFAULT '[]',
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    
    def create_user(self, username, email, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                      (username, email, password))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    
    def get_user_by_username(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def update_user_coins(self, username, coin_change):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET coins = coins + ? WHERE username = ?",
                      (coin_change, username))
        conn.commit()
        conn.close()
    
    def create_session(self, username, start_time, end_time, total_duration,
                      breaks, net_study_time, improvements, mistakes,
                      ai_rating, ai_suggestions, coins_earned, subject):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sessions (username, start_time, end_time, total_duration, breaks,
                                net_study_time, improvements, mistakes, ai_rating,
                                ai_suggestions, coins_earned, subject)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, start_time, end_time, total_duration, breaks,
              net_study_time, improvements, mistakes, ai_rating,
              ai_suggestions, coins_earned, subject))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id
    
    def get_user_sessions(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE username = ? ORDER BY start_time DESC",
                      (username,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_active_rooms(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM study_rooms WHERE is_active = 1")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
'''

print("✅ Created database.py")
print(f"   Size: {len(database_py):,} bytes")
