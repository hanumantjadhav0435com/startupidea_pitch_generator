# AI Pitch Generator - Local Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL database (optional - can use SQLite for development)

## Installation Steps

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd ai-pitch-generator
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Login==0.6.3
pip install Flask-Mail==0.9.1
pip install Flask-WTF==1.2.1
pip install WTForms==3.1.1
pip install Werkzeug==3.0.1
pip install SQLAlchemy==2.0.23
pip install email-validator==2.1.0
pip install google-genai==0.4.0
pip install pydantic==2.5.2
pip install python-pptx==0.6.23
pip install gunicorn==21.2.0
pip install psycopg2-binary==2.9.9
```

Or install all at once:
```bash
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Flask-Mail==0.9.1 Flask-WTF==1.2.1 WTForms==3.1.1 Werkzeug==3.0.1 SQLAlchemy==2.0.23 email-validator==2.1.0 google-genai==0.4.0 pydantic==2.5.2 python-pptx==0.6.23 gunicorn==21.2.0 psycopg2-binary==2.9.9
```

### 4. Environment Configuration

Create a `.env` file in the root directory:
```bash
# Database Configuration
DATABASE_URL=sqlite:///pitch_generator.db  # For SQLite
# DATABASE_URL=postgresql://username:password@localhost/pitch_generator  # For PostgreSQL

# Session Security
SESSION_SECRET=your-secret-key-here-change-this-in-production

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Email Configuration (Optional - for password reset)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 5. Database Setup

#### For SQLite (Default)
The database will be created automatically when you run the application.

#### For PostgreSQL (Optional)
```bash
# Create database
createdb pitch_generator

# Update DATABASE_URL in .env file
DATABASE_URL=postgresql://username:password@localhost/pitch_generator
```

### 6. Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

### 7. Run the Application

#### Development Mode
```bash
python app.py
```

#### Production Mode
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

The application will be available at `http://localhost:5000`

## File Structure

```
ai-pitch-generator/
├── app.py              # Main Flask application
├── main.py             # Application entry point
├── models.py           # Database models
├── auth.py             # Authentication routes
├── forms.py            # WTForms definitions
├── pitch_generator.py  # AI pitch generation logic
├── ppt_generator.py    # PowerPoint creation
├── email_utils.py      # Email functionality
├── static/             # CSS, JS, images
├── templates/          # HTML templates
├── .env               # Environment variables
└── SETUP.md           # This file
```

## Features

- **User Authentication**: Registration, login, password reset
- **AI Pitch Generation**: Powered by Google Gemini API
- **PowerPoint Export**: Download generated pitches as PPT files
- **Responsive Design**: Works on desktop and mobile
- **Fallback System**: Works even when AI service is unavailable

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check your DATABASE_URL in `.env`
   - Ensure PostgreSQL is running (if using PostgreSQL)

2. **Gemini API Error**
   - Verify your GEMINI_API_KEY is correct
   - Check your API quota and billing

3. **Email Not Working**
   - Configure MAIL_* variables in `.env`
   - Use app-specific passwords for Gmail

4. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility

### Debug Mode

To enable debug logging, add this to your `.env`:
```
FLASK_DEBUG=1
```

## Production Deployment

For production deployment:

1. Use a proper database (PostgreSQL)
2. Set strong SESSION_SECRET
3. Configure proper email settings
4. Use environment variables for all secrets
5. Use gunicorn or similar WSGI server
6. Set up reverse proxy (nginx)
7. Enable HTTPS

## Support

If you encounter issues:
1. Check the console logs for error messages
2. Verify all environment variables are set
3. Ensure API keys are valid and have quota
4. Check database connectivity

## License

This project is for educational and development purposes.