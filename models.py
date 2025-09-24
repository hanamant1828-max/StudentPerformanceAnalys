from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):  # type: ignore
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='student')  # student, teacher, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    active_status = db.Column(db.Boolean, default=True)  # renamed to avoid UserMixin conflict
    
    # Relationships
    predictions = db.relationship('PredictionHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.username}>'

class PredictionHistory(db.Model):  # type: ignore
    __tablename__ = 'prediction_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    student_name = db.Column(db.String(200), nullable=False)
    predicted_performance = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    
    # Input features
    previous_grades = db.Column(db.Float, nullable=False)
    attendance_percentage = db.Column(db.Float, nullable=False)
    study_hours_per_day = db.Column(db.Float, nullable=False)
    extracurricular_activities = db.Column(db.Integer, nullable=False)
    interactiveness = db.Column(db.Boolean, nullable=False)
    practical_knowledge = db.Column(db.String(20), nullable=False)
    communication_skill = db.Column(db.String(20), nullable=False)
    projects_handled = db.Column(db.Integer, nullable=False)
    assignments_completed = db.Column(db.Integer, nullable=False)
    
    # Metadata
    prediction_type = db.Column(db.String(20), default='single')  # single or batch
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert prediction to dictionary"""
        return {
            'id': self.id,
            'student_name': self.student_name,
            'predicted_performance': self.predicted_performance,
            'confidence': self.confidence,
            'previous_grades': self.previous_grades,
            'attendance_percentage': self.attendance_percentage,
            'study_hours_per_day': self.study_hours_per_day,
            'extracurricular_activities': self.extracurricular_activities,
            'interactiveness': self.interactiveness,
            'practical_knowledge': self.practical_knowledge,
            'communication_skill': self.communication_skill,
            'projects_handled': self.projects_handled,
            'assignments_completed': self.assignments_completed,
            'prediction_type': self.prediction_type,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<PredictionHistory {self.student_name}: {self.predicted_performance}>'