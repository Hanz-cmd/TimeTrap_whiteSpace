
# 3. Requirements file
requirements = '''Flask==3.0.0
Flask-CORS==4.0.0
'''

# 4. Startup script for Windows
run_bat = '''@echo off
echo Starting StudyFlow Backend...
python app.py
pause
'''

# 5. Startup script for Mac/Linux
run_sh = '''#!/bin/bash
echo "Starting StudyFlow Backend..."
python3 app.py
'''

print("✅ Created requirements.txt")
print("✅ Created run.bat (Windows)")
print("✅ Created run.sh (Mac/Linux)")
