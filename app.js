// StudyFlow Enhanced - Complete JavaScript
// API Configuration
const API_URL = 'https://aahans.pythonanywhere.com/api';
let currentUser = null;
let sessionStartTime = null;
let sessionTimer = null;
let sessionSeconds = 0;
let weeklyChart = null;
let ratingsChart = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    checkLogin();
    loadTheme();
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
        const shopBalance = document.getElementById('shopCoinBalance');
        if (shopBalance) shopBalance.textContent = currentUser.coins || 0;
    }
}

// ==================== AUTH FUNCTIONS ====================
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

        alert('Welcome to StudyFlow! Start studying to earn coins!');
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

// ==================== THEME TOGGLE ====================
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    document.body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);

    if (document.getElementById('analyticsPage').style.display !== 'none') {
        loadAnalytics();
    }
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.textContent = theme === 'light' ? '🌙' : '☀️';
    }
}

// ==================== PAGE NAVIGATION ====================
function showPage(pageName) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.style.display = 'none');

    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => btn.classList.remove('active'));

    const selectedPage = document.getElementById(pageName + 'Page');
    if (selectedPage) {
        selectedPage.style.display = 'block';
    }

    if (event && event.target) {
        event.target.classList.add('active');
    }

    if (pageName === 'dashboard') loadDashboard();
    if (pageName === 'analytics') loadAnalytics();
    if (pageName === 'rooms') loadRooms();
}

// ==================== DASHBOARD ====================
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

        const avgRating = sessions.length > 0 
            ? Math.round(sessions.reduce((sum, s) => sum + s.ai_rating, 0) / sessions.length)
            : 0;
        document.getElementById('avgRating').textContent = avgRating;

    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// ==================== TIMER ====================
function startSession() {
    sessionStartTime = new Date().toISOString();
    sessionSeconds = 0;

    sessionTimer = setInterval(() => {
        sessionSeconds++;
        updateTimerDisplay();
    }, 1000);

    document.getElementById('startSessionBtn').style.display = 'none';
    document.getElementById('endSessionBtn').style.display = 'inline-block';

    alert('Focus time started! Make every second count!');
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
                aiSuggestions: 'Great work!',
                coinsEarned: sessionData.coinsEarned,
                subject: ''
            })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser.coins += sessionData.coinsEarned;
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            updateUserDisplay();

            alert(`Amazing session! You earned ${sessionData.coinsEarned} coins!`);

            sessionSeconds = 0;
            updateTimerDisplay();
            document.getElementById('startSessionBtn').style.display = 'inline-block';
            document.getElementById('endSessionBtn').style.display = 'none';

            loadDashboard();
        }
    } catch (error) {
        alert('Error saving session: ' + error.message);
    }
}

function updateTimerDisplay() {
    const hours = Math.floor(sessionSeconds / 3600);
    const minutes = Math.floor((sessionSeconds % 3600) / 60);
    const secs = sessionSeconds % 60;

    const display = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    document.getElementById('sessionTimer').textContent = display;
}

// ==================== ANALYTICS & CHARTS ====================
async function loadAnalytics() {
    try {
        const response = await fetch(`${API_URL}/sessions/${currentUser.username}`);
        const sessions = await response.json();

        createWeeklyChart(sessions);
        createRatingsChart(sessions);
        displaySessionsList(sessions);

    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

function createWeeklyChart(sessions) {
    const ctx = document.getElementById('weeklyChart');

    if (weeklyChart) {
        weeklyChart.destroy();
    }

    const weekData = getWeeklyData(sessions);
    const theme = document.body.getAttribute('data-theme');
    const textColor = theme === 'dark' ? '#ffffff' : '#333333';
    const gridColor = theme === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';

    weeklyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Study Hours',
                data: weekData,
                backgroundColor: 'rgba(102, 126, 234, 0.6)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: { color: textColor }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                },
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                }
            }
        }
    });
}

function createRatingsChart(sessions) {
    const ctx = document.getElementById('ratingsChart');

    if (ratingsChart) {
        ratingsChart.destroy();
    }

    const ratings = sessions.slice(0, 10).map(s => s.ai_rating).reverse();
    const labels = sessions.slice(0, 10).map((s, i) => `S${i + 1}`).reverse();
    const theme = document.body.getAttribute('data-theme');
    const textColor = theme === 'dark' ? '#ffffff' : '#333333';
    const gridColor = theme === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';

    ratingsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Rating',
                data: ratings,
                borderColor: 'rgba(118, 75, 162, 1)',
                backgroundColor: 'rgba(118, 75, 162, 0.2)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: { color: textColor }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                },
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                }
            }
        }
    });
}

function getWeeklyData(sessions) {
    const weekData = [0, 0, 0, 0, 0, 0, 0];
    const now = new Date();
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

    sessions.forEach(session => {
        const sessionDate = new Date(session.start_time);
        if (sessionDate >= weekAgo) {
            const dayIndex = sessionDate.getDay();
            const adjustedIndex = dayIndex === 0 ? 6 : dayIndex - 1;
            weekData[adjustedIndex] += session.net_study_time / 3600;
        }
    });

    return weekData.map(hours => Math.round(hours * 10) / 10);
}

function displaySessionsList(sessions) {
    const listEl = document.getElementById('sessionsList');
    listEl.innerHTML = '<h3>Recent Sessions</h3>';

    if (sessions.length === 0) {
        listEl.innerHTML += '<p class="loading-text">No sessions yet. Start studying!</p>';
        return;
    }

    sessions.slice(0, 10).forEach(session => {
        const date = new Date(session.start_time).toLocaleString();
        const duration = Math.floor(session.net_study_time / 60);

        listEl.innerHTML += `
            <div class="session-item">
                <h4>${date}</h4>
                <p>Duration: ${duration} min | Rating: ${session.ai_rating}/100 | Coins: ${session.coins_earned}</p>
            </div>
        `;
    });
}

// ==================== SHOP ====================
async function purchaseItem(itemName, cost) {
    if (currentUser.coins < cost) {
        alert('Not enough coins! Keep studying to earn more!');
        return;
    }

    if (!confirm(`Purchase "${itemName}" for ${cost} coins?`)) {
        return;
    }

    try {
        currentUser.coins -= cost;
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        updateUserDisplay();

        alert(`You purchased "${itemName}"! Enjoy your reward!`);

    } catch (error) {
        alert('Purchase failed: ' + error.message);
    }
}

// ==================== STUDY ROOMS ====================
async function loadRooms() {
    try {
        const response = await fetch(`${API_URL}/rooms`);
        const rooms = await response.json();

        const listEl = document.getElementById('roomsList');
        listEl.innerHTML = '';

        if (rooms.length === 0) {
            listEl.innerHTML = '<p class="loading-text">No active rooms. Create one!</p>';
            return;
        }

        rooms.forEach(room => {
            const participants = JSON.parse(room.participants || '[]');
            listEl.innerHTML += `
                <div class="room-card">
                    <h3>${room.name}</h3>
                    <p>${room.description || 'No description'}</p>
                    <div class="room-participants">
                        ${participants.length}/${room.max_participants} participants
                    </div>
                    <button class="btn-join" onclick="joinRoom(${room.id})">Join Room</button>
                </div>
            `;
        });

    } catch (error) {
        console.error('Error loading rooms:', error);
    }
}

function showCreateRoomModal() {
    document.getElementById('createRoomModal').style.display = 'flex';
}

function closeCreateRoomModal() {
    document.getElementById('createRoomModal').style.display = 'none';
}

async function createRoom() {
    const name = document.getElementById('roomName').value.trim();
    const description = document.getElementById('roomDescription').value.trim();
    const maxPart = parseInt(document.getElementById('roomMaxPart').value);

    if (!name) {
        alert('Please enter a room name');
        return;
    }

    closeCreateRoomModal();
    alert('Room created! Study with friends!');
    loadRooms();
}

async function joinRoom(roomId) {
    alert('Joining room... Feature coming soon with WebRTC!');
}

console.log('StudyFlow Enhanced loaded. Backend:', API_URL);
