from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_token = db.Column(db.String(256))
    reset_token_expires = db.Column(db.DateTime)
    
    # Relationships
    pitches = db.relationship('Pitch', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Pitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    startup_idea = db.Column(db.Text, nullable=False)
    pitch_data_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def pitch_data(self):
        try:
            return json.loads(self.pitch_data_json)
        except:
            return {}
    
    @pitch_data.setter
    def pitch_data(self, value):
        self.pitch_data_json = json.dumps(value)
    
    def __repr__(self):
        return f'<Pitch {self.id}>'
