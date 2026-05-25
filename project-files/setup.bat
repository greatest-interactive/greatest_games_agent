@echo off
REM Quick Start Script for Greatest Game Agent (Windows)
REM Run this from the project-files directory

echo.
echo 🎮 Greatest Game Agent - Quick Setup
echo ======================================
echo.

echo ✓ Checking Python...
python --version

echo ✓ Checking Node.js...
node --version

echo.
echo 📦 Installing Backend Dependencies...
cd backend
if not exist "venv" (
  python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo 📦 Installing Frontend Dependencies...
cd ..\frontend
call npm install

echo.
echo ✅ Setup Complete!
echo.
echo Next Steps:
echo 1. Create .env file in backend\ with your API keys
echo 2. Run migrations: cd backend ^&^& python manage.py migrate
echo 3. Create superuser: python manage.py createsuperuser
echo 4. Start backend: python manage.py runserver
echo 5. In new terminal, start frontend: cd frontend ^&^& npm start
echo.
echo Application will be at http://localhost:3000
echo.
pause
