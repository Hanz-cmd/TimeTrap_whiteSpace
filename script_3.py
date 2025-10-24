
# 6. Complete HTML Frontend
index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudyFlow - Gamified Study Productivity</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- AUTH PAGE -->
    <div id="authPage" style="display: flex;">
        <div class="auth-container">
            <h1 class="auth-title">StudyFlow</h1>
            
            <!-- LOGIN FORM -->
            <div id="loginFormContainer" style="display: block;">
                <h2>Login</h2>
                <form id="loginForm" onsubmit="event.preventDefault(); login();">
                    <div class="form-group">
                        <label>Username</label>
                        <input type="text" id="loginUsername" required>
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" id="loginPassword" required>
                    </div>
                    <button type="submit" class="btn-primary">Login</button>
                </form>
                <p class="auth-switch">
                    Don't have an account? <a href="#" onclick="showSignupForm(); return false;">Sign Up</a>
                </p>
            </div>
            
            <!-- SIGNUP FORM -->
            <div id="signupFormContainer" style="display: none;">
                <h2>Create Account</h2>
                <form id="signupForm" onsubmit="event.preventDefault(); signup();">
                    <div class="form-group">
                        <label>Username</label>
                        <input type="text" id="signupUsername" required>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" id="signupEmail" required>
                    </div>
                    <div class="form-group">
                        <label>Password (min 8 characters)</label>
                        <input type="password" id="signupPassword" required minlength="8">
                    </div>
                    <button type="submit" class="btn-primary">Create Account</button>
                </form>
                <p class="auth-switch">
                    Already have an account? <a href="#" onclick="showLoginForm(); return false;">Login</a>
                </p>
            </div>
        </div>
    </div>

    <!-- APP CONTAINER -->
    <div id="appContainer" style="display: none;">
        <!-- HEADER -->
        <header class="app-header">
            <div class="header-content">
                <h1>StudyFlow</h1>
                <div class="header-right">
                    <span class="user-info">
                        <span id="usernameDisplay">User</span>
                        <span class="coin-badge">🪙 <span id="coinBalance">0</span></span>
                    </span>
                    <button onclick="logout()" class="btn-secondary">Logout</button>
                </div>
            </div>
        </header>

        <!-- NAVIGATION -->
        <nav class="app-nav">
            <button onclick="showPage('dashboard')" class="nav-btn">Dashboard</button>
            <button onclick="showPage('timer')" class="nav-btn">Timer</button>
            <button onclick="showPage('analytics')" class="nav-btn">Analytics</button>
        </nav>

        <!-- PAGES -->
        <main class="app-main">
            <!-- DASHBOARD PAGE -->
            <div id="dashboardPage" class="page">
                <h2>Dashboard</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Total Sessions</h3>
                        <p class="stat-value" id="totalSessions">0</p>
                    </div>
                    <div class="stat-card">
                        <h3>Total Study Time</h3>
                        <p class="stat-value" id="totalStudyTime">0h 0m</p>
                    </div>
                    <div class="stat-card">
                        <h3>Coins Earned</h3>
                        <p class="stat-value" id="totalCoins">0</p>
                    </div>
                </div>
            </div>

            <!-- TIMER PAGE -->
            <div id="timerPage" class="page" style="display: none;">
                <h2>Study Timer</h2>
                <div class="timer-container">
                    <div class="timer-display" id="sessionTimer">00:00:00</div>
                    <div class="timer-controls">
                        <button id="startSessionBtn" onclick="startSession()" class="btn-primary btn-large">Start Session</button>
                        <button id="endSessionBtn" onclick="endSession()" class="btn-danger btn-large" style="display: none;">End Session</button>
                    </div>
                </div>
            </div>

            <!-- ANALYTICS PAGE -->
            <div id="analyticsPage" class="page" style="display: none;">
                <h2>Analytics</h2>
                <div id="sessionsList" class="sessions-list"></div>
            </div>
        </main>
    </div>

    <script src="app.js"></script>
</body>
</html>
'''

print("✅ Created index.html")
print(f"   Size: {len(index_html):,} bytes")
