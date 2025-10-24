
# 8. Complete JavaScript Frontend
app_js = '''// API Configuration
const API_URL = 'http://localhost:5000/api';
let currentUser = null;
let sessionStartTime = null;
let sessionTimer = null;
let sessionSeconds = 0;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    checkLogin();
});

function checkLogin() {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        showApp();
        loadDashboard();
    } else {
        showAuthPage();
    }
}

function showAuthPage() {
    document.getElementById('authPage').style.display = 'flex';
    document.getElementById('appContainer').style.display = 'none';
}

function showApp() {
    document.getElementById('authPage').style.display = 'none';
    document.getElementById('appContainer').style.display = 'block';
    updateUserDisplay();
}

function updateUserDisplay() {
    if (currentUser) {
        document.getElementById('usernameDisplay').textContent = currentUser.username;
        document.getElementById('coinBalance').textContent = currentUser.coins || 0;
    }
}

// Auth Functions
function showSignupForm() {
    document.getElementById('loginFormContainer').style.display = 'none';
    document.getElementById('signupFormContainer').style.display = 'block';
}

function showLoginForm() {
    document.getElementById('signupFormContainer').style.display = 'none';
    document.getElementById('loginFormContainer').style.display = 'block';
}

async function signup() {
    const username = document.getElementById('signupUsername').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    
    if (!username || !email || !password) {
        alert('Please fill all fields');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/auth/signup`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, email, password})
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Signup failed');
            return;
        }
        
        currentUser = data.user;
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        
        alert('Account created successfully! Welcome to StudyFlow!');
        showApp();
        loadDashboard();
        
    } catch (error) {
        alert('Error: ' + error.message);
        console.error('Signup error:', error);
    }
}

async function login() {
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;
    
    if (!username || !password) {
        alert('Please enter username and password');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Login failed');
            return;
        }
        
        currentUser = data.user;
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        
        alert('Welcome back, ' + currentUser.username + '!');
        showApp();
        loadDashboard();
        
    } catch (error) {
        alert('Error: ' + error.message);
        console.error('Login error:', error);
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    showAuthPage();
}

// Page Navigation
function showPage(pageName) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.style.display = 'none');
    
    const selectedPage = document.getElementById(pageName + 'Page');
    if (selectedPage) {
        selectedPage.style.display = 'block';
    }
    
    if (pageName === 'dashboard') loadDashboard();
    if (pageName === 'analytics') loadAnalytics();
}

// Dashboard
async function loadDashboard() {
    try {
        const response = await fetch(`${API_URL}/sessions/${currentUser.username}`);
        const sessions = await response.json();
        
        document.getElementById('totalSessions').textContent = sessions.length;
        
        const totalTime = sessions.reduce((sum, s) => sum + s.net_study_time, 0);
        const hours = Math.floor(totalTime / 3600);
        const minutes = Math.floor((totalTime % 3600) / 60);
        document.getElementById('totalStudyTime').textContent = `${hours}h ${minutes}m`;
        
        const totalCoins = sessions.reduce((sum, s) => sum + s.coins_earned, 0);
        document.getElementById('totalCoins').textContent = totalCoins;
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Timer Functions
function startSession() {
    sessionStartTime = new Date().toISOString();
    sessionSeconds = 0;
    
    sessionTimer = setInterval(() => {
        sessionSeconds++;
        updateTimerDisplay();
    }, 1000);
    
    document.getElementById('startSessionBtn').style.display = 'none';
    document.getElementById('endSessionBtn').style.display = 'inline-block';
    
    alert('Study session started! Focus on your goals!');
}

function endSession() {
    clearInterval(sessionTimer);
    
    const endTime = new Date().toISOString();
    const totalDuration = sessionSeconds;
    const minutes = totalDuration / 60;
    
    let rating = 50;
    if (minutes >= 45) rating = 90;
    else if (minutes >= 30) rating = 75;
    else if (minutes >= 15) rating = 60;
    
    const coinsEarned = Math.floor(minutes / 60) * 5;
    
    saveSession({
        startTime: sessionStartTime,
        endTime: endTime,
        totalDuration: totalDuration,
        netStudyTime: totalDuration,
        aiRating: rating,
        coinsEarned: coinsEarned
    });
}

async function saveSession(sessionData) {
    try {
        const response = await fetch(`${API_URL}/sessions`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                username: currentUser.username,
                startTime: sessionData.startTime,
                endTime: sessionData.endTime,
                totalDuration: sessionData.totalDuration,
                breaks: [],
                netStudyTime: sessionData.netStudyTime,
                improvements: '',
                mistakes: '',
                aiRating: sessionData.aiRating,
                aiSuggestions: 'Great session!',
                coinsEarned: sessionData.coinsEarned,
                subject: ''
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser.coins += sessionData.coinsEarned;
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            updateUserDisplay();
            
            alert(`Session saved! You earned ${sessionData.coinsEarned} coins!`);
            
            sessionSeconds = 0;
            updateTimerDisplay();
            document.getElementById('startSessionBtn').style.display = 'inline-block';
            document.getElementById('endSessionBtn').style.display = 'none';
            
            loadDashboard();
        }
    } catch (error) {
        alert('Error saving session: ' + error.message);
        console.error('Session save error:', error);
    }
}

function updateTimerDisplay() {
    const hours = Math.floor(sessionSeconds / 3600);
    const minutes = Math.floor((sessionSeconds % 3600) / 60);
    const secs = sessionSeconds % 60;
    
    const display = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    document.getElementById('sessionTimer').textContent = display;
}

// Analytics
async function loadAnalytics() {
    try {
        const response = await fetch(`${API_URL}/sessions/${currentUser.username}`);
        const sessions = await response.json();
        
        const listEl = document.getElementById('sessionsList');
        listEl.innerHTML = '<h3>Recent Sessions</h3>';
        
        if (sessions.length === 0) {
            listEl.innerHTML += '<p>No sessions yet. Start studying to see your progress!</p>';
            return;
        }
        
        sessions.slice(0, 10).forEach(session => {
            const date = new Date(session.start_time).toLocaleString();
            const duration = Math.floor(session.net_study_time / 60);
            
            listEl.innerHTML += `
                <div class="session-item">
                    <h4>${date}</h4>
                    <p>Duration: ${duration} minutes</p>
                    <p>Rating: ${session.ai_rating}/100</p>
                    <p>Coins Earned: ${session.coins_earned}</p>
                </div>
            `;
        });
        
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

console.log('StudyFlow app loaded. Backend:', API_URL);
'''

print("✅ Created app.js")
print(f"   Size: {len(app_js):,} bytes")
