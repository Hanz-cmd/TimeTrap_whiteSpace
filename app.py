from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import Database
import secrets
from datetime import datetime
import json
import os

# Initialize Flask with template and static folders
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

db = Database()

# ==================== SERVE FRONTEND ====================
@app.route('/')
def index():
    """Serve the main frontend page"""
    return render_template('index.html')

# ==================== AUTH ROUTES ====================
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

# ==================== SESSION ROUTES ====================
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

# ==================== FLASHCARD ROUTES ====================
@app.route('/api/flashcards/generate', methods=['POST'])
def generate_flashcards():
    data = request.json
    username = data.get('username')
    topic = data.get('topic')
    subject = data.get('subject')
    count = int(data.get('count', 5))
    
    flashcards = []
    templates = [
        ("What is {}?", "Definition of {}"),
        ("Explain {} in simple terms.", "Simple explanation of {}"),
        ("What are the main features of {}?", "Key features of {}"),
        ("Give an example of {}.", "Example: {}"),
        ("Why is {} important?", "Importance of {}")
    ]
    
    for i in range(min(count, len(templates))):
        q_template, a_template = templates[i]
        question = q_template.format(topic)
        answer = a_template.format(topic)
        
        flashcard_id = db.create_flashcard(
            username=username,
            subject=subject,
            topic=topic,
            question=question,
            answer=answer,
            difficulty='medium'
        )
        
        flashcards.append({
            'id': flashcard_id,
            'question': question,
            'answer': answer,
            'topic': topic,
            'subject': subject,
            'difficulty': 'medium'
        })
    
    return jsonify({
        'success': True,
        'flashcards': flashcards
    })

@app.route('/api/flashcards/<username>', methods=['GET'])
def get_flashcards(username):
    flashcards = db.get_user_flashcards(username)
    return jsonify(flashcards)

@app.route('/api/flashcards/<int:flashcard_id>/review', methods=['POST'])
def review_flashcard(flashcard_id):
    data = request.json
    correct = data.get('correct', True)
    db.update_flashcard_review(flashcard_id, correct)
    return jsonify({'success': True})

@app.route('/api/flashcards/<int:flashcard_id>', methods=['DELETE'])
def delete_flashcard(flashcard_id):
    db.delete_flashcard(flashcard_id)
    return jsonify({'success': True})

# ==================== ROOMS ROUTES ====================
@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = db.get_active_rooms()
    return jsonify(rooms)

# ==================== RUN SERVER ====================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 50)
    print("StudyFlow Server Starting...")
    print("=" * 50)
    print(f"Server running on port: {port}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=False)
