@echo off
REM AI Pitch Generator - Quick Installation Script for Windows

echo 🚀 AI Pitch Generator - Quick Setup
echo ===================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install packages
echo 📥 Installing dependencies...
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Flask-Mail==0.9.1 Flask-WTF==1.2.1 WTForms==3.1.1 Werkzeug==3.0.1 SQLAlchemy==2.0.23 email-validator==2.1.0 google-genai==0.4.0 pydantic==2.5.2 python-pptx==0.6.23 gunicorn==21.2.0 psycopg2-binary==2.9.9

REM Create .env file if it doesn't exist
if not exist .env (
    echo 🔐 Creating .env file...
    (
        echo # Database Configuration
        echo DATABASE_URL=sqlite:///pitch_generator.db
        echo.
        echo # Session Security ^(Change this in production!^)
        echo SESSION_SECRET=your-secret-key-change-this-in-production
        echo.
        echo # Google Gemini API ^(Required^)
        echo GEMINI_API_KEY=your-gemini-api-key-here
        echo.
        echo # Email Configuration ^(Optional - for password reset^)
        echo MAIL_SERVER=smtp.gmail.com
        echo MAIL_PORT=587
        echo MAIL_USE_TLS=True
        echo MAIL_USERNAME=your-email@gmail.com
        echo MAIL_PASSWORD=your-app-password
    ) > .env
    echo ⚠️  Please edit .env file and add your GEMINI_API_KEY
)

echo.
echo ✅ Installation complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your Google Gemini API key
echo 2. Run: venv\Scripts\activate
echo 3. Run: python app.py
echo 4. Open: http://localhost:5000
echo.
echo 📖 See SETUP.md for detailed instructions
pause