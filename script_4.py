
# 7. CSS Styles
styles_css = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* AUTH PAGE */
#authPage {
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.auth-container {
    background: white;
    padding: 3rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    max-width: 400px;
    width: 90%;
}

.auth-title {
    text-align: center;
    color: #667eea;
    font-size: 2.5rem;
    margin-bottom: 2rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
    font-weight: 500;
}

.form-group input {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.form-group input:focus {
    outline: none;
    border-color: #667eea;
}

.btn-primary {
    width: 100%;
    padding: 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s;
}

.btn-primary:hover {
    transform: translateY(-2px);
}

.auth-switch {
    text-align: center;
    margin-top: 1.5rem;
    color: #666;
}

.auth-switch a {
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
}

/* APP CONTAINER */
.app-header {
    background: white;
    padding: 1rem 2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
}

.header-content h1 {
    color: #667eea;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.coin-badge {
    background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: bold;
    color: #333;
}

.btn-secondary {
    padding: 0.5rem 1.5rem;
    background: #f0f0f0;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
}

.btn-secondary:hover {
    background: #e0e0e0;
}

/* NAVIGATION */
.app-nav {
    background: white;
    padding: 1rem 2rem;
    display: flex;
    gap: 1rem;
    max-width: 1200px;
    margin: 0 auto;
    border-bottom: 2px solid #f0f0f0;
}

.nav-btn {
    padding: 0.75rem 1.5rem;
    background: transparent;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 500;
    transition: background 0.3s;
}

.nav-btn:hover {
    background: #f0f0f0;
}

/* MAIN CONTENT */
.app-main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 2rem;
}

.page {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
}

.stat-card h3 {
    font-size: 1rem;
    margin-bottom: 1rem;
    opacity: 0.9;
}

.stat-value {
    font-size: 2.5rem;
    font-weight: bold;
}

/* TIMER */
.timer-container {
    text-align: center;
    padding: 3rem;
}

.timer-display {
    font-size: 5rem;
    font-weight: bold;
    color: #667eea;
    margin: 2rem 0;
    font-family: 'Courier New', monospace;
}

.timer-controls {
    display: flex;
    justify-content: center;
    gap: 1rem;
}

.btn-large {
    padding: 1.5rem 3rem;
    font-size: 1.2rem;
}

.btn-danger {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
}

.btn-danger:hover {
    transform: translateY(-2px);
}

/* SESSIONS LIST */
.sessions-list {
    margin-top: 2rem;
}

.session-item {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border-left: 4px solid #667eea;
}

.session-item h4 {
    color: #333;
    margin-bottom: 0.5rem;
}

.session-item p {
    color: #666;
    margin: 0.25rem 0;
}
'''

print("✅ Created styles.css")
print(f"   Size: {len(styles_css):,} bytes")
