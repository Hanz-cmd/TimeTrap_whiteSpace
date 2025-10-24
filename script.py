
import zipfile
import io

# Create all the files needed for a complete working app

# 1. Flask Backend (app.py)
app_py = '''from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
import secrets
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

db = Database()

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    if db.get_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400
    
    user_id = db.create_user(username, email, password)
    token = secrets.token_urlsafe(32)
    
    return jsonify({
        'success': True,
        'user': {
            'id': user_id,
            'username': username,
            'email': email,
            'coins': 0,
            'theme': 'light'
        },
        'token': token
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    user = db.get_user_by_username(username)
    
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    token = secrets.token_urlsafe(32)
    
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'coins': user['coins'],
            'theme': user['theme']
        },
        'token': token
    })

@app.route('/api/sessions', methods=['POST'])
def create_session():
    data = request.json
    
    session_id = db.create_session(
        username=data['username'],
        start_time=data['startTime'],
        end_time=data['endTime'],
        total_duration=data['totalDuration'],
        breaks=json.dumps(data.get('breaks', [])),
        net_study_time=data['netStudyTime'],
        improvements=data.get('improvements', ''),
        mistakes=data.get('mistakes', ''),
        ai_rating=data['aiRating'],
        ai_suggestions=data['aiSuggestions'],
        coins_earned=data['coinsEarned'],
        subject=data.get('subject', '')
    )
    
    db.update_user_coins(data['username'], data['coinsEarned'])
    
    return jsonify({
        'success': True,
        'sessionId': session_id,
        'coinsEarned': data['coinsEarned']
    })

@app.route('/api/sessions/<username>', methods=['GET'])
def get_user_sessions(username):
    sessions = db.get_user_sessions(username)
    for session in sessions:
        session['breaks'] = json.loads(session['breaks'])
    return jsonify(sessions)

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = db.get_active_rooms()
    return jsonify(rooms)

if __name__ == '__main__':
    print("=" * 50)
    print("StudyFlow Backend Server Starting...")
    print("=" * 50)
    print("Server: http://localhost:5000")
    print("API: http://localhost:5000/api")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=False)
'''

print("✅ Created app.py (Flask backend)")
print(f"   Size: {len(app_py):,} bytes")
