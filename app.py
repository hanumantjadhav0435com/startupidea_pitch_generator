import os
import logging
from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_mail import Mail
from werkzeug.middleware.proxy_fix import ProxyFix
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///pitch_generator.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Mail configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

mail = Mail(app)

# Import routes after app creation
from auth import auth_bp
from pitch_generator import generate_pitch_content
from ppt_generator import create_pitch_ppt

app.register_blueprint(auth_bp)

with app.app_context():
    import models
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    from models import Pitch
    user_pitches = Pitch.query.filter_by(user_id=current_user.id).order_by(Pitch.created_at.desc()).all()
    return render_template('dashboard.html', pitches=user_pitches)

@app.route('/generate')
@login_required
def generate():
    return render_template('generate_pitch.html')

@app.route('/api/generate_pitch', methods=['POST'])
@login_required
def api_generate_pitch():
    try:
        data = request.get_json()
        startup_idea = data.get('idea', '').strip()
        
        if not startup_idea:
            return jsonify({'error': 'Startup idea is required'}), 400
        
        # Generate pitch content using Gemini
        pitch_data = generate_pitch_content(startup_idea)
        
        # Save to database
        from models import Pitch
        pitch = Pitch(
            user_id=current_user.id,
            startup_idea=startup_idea,
            pitch_data=pitch_data
        )
        db.session.add(pitch)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'pitch_id': pitch.id,
            'data': pitch_data
        })
        
    except Exception as e:
        logging.error(f"Error generating pitch: {str(e)}")
        return jsonify({'error': 'Failed to generate pitch. Please try again.'}), 500

@app.route('/api/download_ppt/<int:pitch_id>')
@login_required
def download_ppt(pitch_id):
    try:
        from models import Pitch
        pitch = Pitch.query.filter_by(id=pitch_id, user_id=current_user.id).first()
        
        if not pitch:
            flash('Pitch not found', 'error')
            return redirect(url_for('dashboard'))
        
        # Generate PowerPoint file
        ppt_path = create_pitch_ppt(pitch.pitch_data, pitch.startup_idea)
        
        return send_file(
            ppt_path,
            as_attachment=True,
            download_name=f'startup_pitch_{pitch_id}.pptx',
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        
    except Exception as e:
        logging.error(f"Error downloading PPT: {str(e)}")
        flash('Failed to download presentation. Please try again.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/pitch/<int:pitch_id>')
@login_required
def view_pitch(pitch_id):
    from models import Pitch
    pitch = Pitch.query.filter_by(id=pitch_id, user_id=current_user.id).first()
    
    if not pitch:
        flash('Pitch not found', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('view_pitch.html', pitch=pitch)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
