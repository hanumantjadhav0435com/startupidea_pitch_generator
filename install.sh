#!/bin/bash

# AI Pitch Generator - Quick Installation Script

echo "🚀 AI Pitch Generator - Quick Setup"
echo "==================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install packages
echo "📥 Installing dependencies..."
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Flask-Mail==0.9.1 Flask-WTF==1.2.1 WTForms==3.1.1 Werkzeug==3.0.1 SQLAlchemy==2.0.23 email-validator==2.1.0 google-genai==0.4.0 pydantic==2.5.2 python-pptx==0.6.23 gunicorn==21.2.0 psycopg2-binary==2.9.9

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔐 Creating .env file..."
    cat > .env << EOL
# Database Configuration
DATABASE_URL=sqlite:///pitch_generator.db

# Session Security (Change this in production!)
SESSION_SECRET=your-secret-key-change-this-in-production

# Google Gemini API (Required)
GEMINI_API_KEY=your-gemini-api-key-here

# Email Configuration (Optional - for password reset)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
EOL
    echo "⚠️  Please edit .env file and add your GEMINI_API_KEY"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Google Gemini API key"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python app.py"
echo "4. Open: http://localhost:5000"
echo ""
echo "📖 See SETUP.md for detailed instructions"