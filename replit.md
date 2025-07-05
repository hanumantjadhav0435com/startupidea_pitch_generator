# AI Pitch Generator

## Overview

The AI Pitch Generator is a Flask-based web application that transforms startup ideas into professional investor pitch decks using AI. Users can input their startup concepts and receive comprehensive pitch presentations with the option to download them as PowerPoint files.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite (development) / PostgreSQL (production ready)
- **Authentication**: Flask-Login with session management
- **Email Service**: Flask-Mail for password reset functionality
- **AI Integration**: Google Gemini API for pitch content generation
- **File Generation**: python-pptx for PowerPoint creation

### Frontend Architecture
- **Templates**: Jinja2 templating engine
- **CSS Frameworks**: Bootstrap 5 + Tailwind CSS hybrid approach
- **JavaScript**: Vanilla JS with Bootstrap components
- **Icons**: Font Awesome
- **Responsive Design**: Mobile-first approach

## Key Components

### Authentication System
- User registration and login with Flask-Login
- Password hashing using Werkzeug security
- Password reset functionality with email tokens
- Session management with secure cookies

### Database Models
- **User Model**: Stores user credentials and profile information
- **Pitch Model**: Stores generated pitch data with JSON serialization
- Foreign key relationships between users and their pitches

### AI Integration
- **Gemini API**: Generates comprehensive pitch content
- **Structured Output**: Uses Pydantic models for data validation
- **Content Generation**: Creates 5-slide pitch decks with detailed content

### File Generation
- **PowerPoint Creation**: Generates professional presentations
- **Template System**: Consistent slide layouts and branding
- **Download Management**: Temporary file handling for downloads

## Data Flow

1. **User Input**: User submits startup idea through web form
2. **AI Processing**: Gemini API generates structured pitch content
3. **Data Storage**: Pitch data saved to database with user association
4. **Presentation Generation**: python-pptx creates PowerPoint file
5. **File Delivery**: User downloads generated presentation

## External Dependencies

### Required APIs
- **Google Gemini API**: For AI-powered content generation
- **SMTP Service**: For email functionality (password resets)

### Python Packages
- Flask ecosystem (Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail)
- AI/ML libraries (google-genai, pydantic)
- File processing (python-pptx)
- Security (werkzeug)

### Frontend Libraries
- Bootstrap 5 (UI components)
- Tailwind CSS (utility classes)
- Font Awesome (icons)
- Vanilla JavaScript (interactions)

## Deployment Strategy

### Environment Configuration
- Environment variables for API keys and database URLs
- Separate development and production configurations
- Docker-ready structure with proper secret management

### Database Strategy
- SQLite for development
- PostgreSQL for production (easily configurable)
- Database migrations handled through Flask-Migrate

### Security Considerations
- Password hashing with Werkzeug
- Session security with Flask-Login
- Environment-based secret key management
- CSRF protection through Flask-WTF

## Changelog
- July 05, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.