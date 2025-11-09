import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
from email_validator import validate_email, EmailNotValidError
from models import db, User, PredictionHistory
from ml_model import StudentPerformanceModel
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration - using SQLite strictly
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student_performance.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
CORS(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize ML model
ml_model = StudentPerformanceModel()

# Create database tables and default user
with app.app_context():
    db.create_all()
    logging.info("Database tables created successfully")
    
    # Create default demo user if it doesn't exist
    demo_user = User.query.filter_by(username='demo').first()
    if not demo_user:
        demo_user = User(
            username='demo',
            email='demo@example.com',
            first_name='Demo',
            last_name='User',
            role='student'
        )
        demo_user.set_password('demo123')
        db.session.add(demo_user)
        db.session.commit()
        logging.info("Default demo user created: username='demo', password='demo123'")

# Authentication routes
@app.route('/')
def index():
    """Render the main application page or redirect to login"""
    if current_user.is_authenticated:
        return render_template('index.html', user=current_user)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    logging.info(f"Login route accessed - Method: {request.method}")
    if current_user.is_authenticated:
        logging.info("User already authenticated, redirecting to index")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        logging.info("POST request received to /login")
        data = request.get_json() if request.is_json else request.form
        username = data.get('username', '').strip()
        password = data.get('password', '')
        remember = bool(data.get('remember', False))
        
        logging.info(f"Login attempt for username: {username}")
        
        if not username or not password:
            error = 'Please provide both username and password'
            logging.warning(f"Login failed: missing credentials")
            if request.is_json:
                return jsonify({'error': error}), 400
            flash(error, 'error')
            return render_template('auth/login.html')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        logging.info(f"User found: {user is not None}")
        
        if user and user.check_password(password):
            logging.info(f"Password check passed for user: {username}")
            if not user.active_status:
                error = 'Your account has been deactivated. Please contact an administrator.'
                logging.warning(f"Login failed: account deactivated for {username}")
                if request.is_json:
                    return jsonify({'error': error}), 400
                flash(error, 'error')
                return render_template('auth/login.html')
            
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            logging.info(f"User {username} logged in successfully")
            
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('index')})
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            error = 'Invalid username or password'
            logging.warning(f"Login failed: invalid credentials for {username}")
            if request.is_json:
                return jsonify({'error': error}), 400
            flash(error, 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Get form data
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        role = data.get('role', 'student').strip()
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        elif User.query.filter_by(username=username).first():
            errors.append('Username already exists')
        
        if not email:
            errors.append('Email is required')
        else:
            try:
                validate_email(email)
            except EmailNotValidError:
                errors.append('Invalid email address')
            
            if User.query.filter_by(email=email).first():
                errors.append('Email already registered')
        
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters long')
        elif password != confirm_password:
            errors.append('Passwords do not match')
        
        if not first_name:
            errors.append('First name is required')
        
        if not last_name:
            errors.append('Last name is required')
        
        if role not in ['student', 'teacher', 'admin']:
            role = 'student'
        
        if errors:
            if request.is_json:
                return jsonify({'errors': errors}), 400
            for error in errors:
                flash(error, 'error')
            return render_template('auth/register.html')
        
        # Create new user
        try:
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Auto-login after successful registration
            login_user(user)
            
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('index')})
            
            flash('Registration successful! Welcome to the Student Performance Prediction System.', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Registration error: {str(e)}")
            error = 'Registration failed. Please try again.'
            if request.is_json:
                return jsonify({'error': error}), 500
            flash(error, 'error')
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    # Get user's recent predictions
    recent_predictions = PredictionHistory.query.filter_by(user_id=current_user.id)\
        .order_by(PredictionHistory.created_at.desc()).limit(10).all()
    
    # Get all predictions for statistics
    all_predictions = PredictionHistory.query.filter_by(user_id=current_user.id).all()
    total_predictions = len(all_predictions)
    
    # Calculate performance distribution
    performance_stats = {
        'Excellent': 0,
        'Good': 0,
        'Average': 0,
        'Poor': 0
    }
    
    total_confidence = 0
    for pred in all_predictions:
        if pred.predicted_performance in performance_stats:
            performance_stats[pred.predicted_performance] += 1
        total_confidence += pred.confidence
    
    avg_confidence = (total_confidence / total_predictions * 100) if total_predictions > 0 else 0
    
    # Get batch vs single statistics
    batch_count = PredictionHistory.query.filter_by(user_id=current_user.id, prediction_type='batch').count()
    single_count = PredictionHistory.query.filter_by(user_id=current_user.id, prediction_type='single').count()
    
    return render_template('dashboard.html', 
                         user=current_user, 
                         recent_predictions=recent_predictions,
                         total_predictions=total_predictions,
                         performance_stats=performance_stats,
                         avg_confidence=avg_confidence,
                         batch_count=batch_count,
                         single_count=single_count)

@app.route('/api/predict_single', methods=['POST'])
@login_required
def predict_single():
    """Predict performance for a single student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'student_name', 'previous_grades', 'attendance', 'study_hours',
            'extracurricular_activities', 'interactiveness', 'practical_knowledge',
            'communication_skill', 'projects_handled', 'assignments_completed'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare data for prediction
        student_data = {
            'Previous_Grades': float(data['previous_grades']),
            'Attendance_Percentage': float(data['attendance']),
            'Study_Hours_Per_Day': float(data['study_hours']),
            'Extracurricular_Activities': int(data['extracurricular_activities']),
            'Interactiveness': 1 if data['interactiveness'].lower() == 'yes' else 0,
            'Practical_Knowledge': data['practical_knowledge'],
            'Communication_Skill': data['communication_skill'],
            'Projects_Handled': int(data['projects_handled']),
            'Assignments_Completed': int(data['assignments_completed'])
        }
        
        # Make prediction
        prediction, suggestions = ml_model.predict_single(student_data)
        confidence = ml_model.get_prediction_confidence(student_data)
        
        # Save prediction to history
        try:
            prediction_record = PredictionHistory(
                user_id=current_user.id,
                student_name=data['student_name'],
                predicted_performance=prediction,
                confidence=confidence,
                previous_grades=student_data['Previous_Grades'],
                attendance_percentage=student_data['Attendance_Percentage'],
                study_hours_per_day=student_data['Study_Hours_Per_Day'],
                extracurricular_activities=student_data['Extracurricular_Activities'],
                interactiveness=bool(student_data['Interactiveness']),
                practical_knowledge=student_data['Practical_Knowledge'],
                communication_skill=student_data['Communication_Skill'],
                projects_handled=student_data['Projects_Handled'],
                assignments_completed=student_data['Assignments_Completed'],
                prediction_type='single'
            )
            db.session.add(prediction_record)
            db.session.commit()
        except Exception as e:
            logging.error(f"Error saving prediction history: {str(e)}")
            db.session.rollback()
        
        result = {
            'student_name': data['student_name'],
            'predicted_performance': prediction,
            'suggestions': suggestions,
            'confidence': confidence
        }
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Error in predict_single: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/api/predict_batch', methods=['POST'])
@login_required
def predict_batch():
    """Predict performance for multiple students from Excel file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename or not file.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'Invalid file format. Please upload Excel file (.xlsx or .xls)'}), 400
        
        # Read Excel file
        try:
            df = pd.read_excel(file)
        except Exception as e:
            return jsonify({'error': f'Error reading Excel file: {str(e)}'}), 400
        
        # Validate columns
        required_columns = [
            'Student_Name', 'Previous_Grades', 'Attendance_Percentage', 'Study_Hours_Per_Day',
            'Extracurricular_Activities', 'Interactiveness', 'Practical_Knowledge',
            'Communication_Skill', 'Projects_Handled', 'Assignments_Completed'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({'error': f'Missing columns in Excel file: {", ".join(missing_columns)}'}), 400
        
        # Make predictions for all students
        results = []
        performance_stats = {'Poor': 0, 'Average': 0, 'Good': 0, 'Excellent': 0}
        
        for index, row in df.iterrows():
            try:
                student_data = {
                    'Previous_Grades': float(row['Previous_Grades']),
                    'Attendance_Percentage': float(row['Attendance_Percentage']),
                    'Study_Hours_Per_Day': float(row['Study_Hours_Per_Day']),
                    'Extracurricular_Activities': int(row['Extracurricular_Activities']),
                    'Interactiveness': 1 if str(row['Interactiveness']).lower() == 'yes' else 0,
                    'Practical_Knowledge': str(row['Practical_Knowledge']),
                    'Communication_Skill': str(row['Communication_Skill']),
                    'Projects_Handled': int(row['Projects_Handled']),
                    'Assignments_Completed': int(row['Assignments_Completed'])
                }
                
                prediction, suggestions = ml_model.predict_single(student_data)
                confidence = ml_model.get_prediction_confidence(student_data)
                performance_stats[prediction] += 1
                
                # Save to prediction history
                try:
                    prediction_record = PredictionHistory(
                        user_id=current_user.id,
                        student_name=str(row['Student_Name']),
                        predicted_performance=prediction,
                        confidence=confidence,
                        previous_grades=student_data['Previous_Grades'],
                        attendance_percentage=student_data['Attendance_Percentage'],
                        study_hours_per_day=student_data['Study_Hours_Per_Day'],
                        extracurricular_activities=student_data['Extracurricular_Activities'],
                        interactiveness=bool(student_data['Interactiveness']),
                        practical_knowledge=student_data['Practical_Knowledge'],
                        communication_skill=student_data['Communication_Skill'],
                        projects_handled=student_data['Projects_Handled'],
                        assignments_completed=student_data['Assignments_Completed'],
                        prediction_type='batch'
                    )
                    db.session.add(prediction_record)
                except Exception as e:
                    logging.error(f"Error saving batch prediction history for row {index}: {str(e)}")
                
                results.append({
                    'student_name': str(row['Student_Name']),
                    'predicted_performance': prediction,
                    'suggestions': suggestions,
                    'confidence': confidence
                })
                
            except Exception as e:
                logging.error(f"Error processing row {index}: {str(e)}")
                results.append({
                    'student_name': str(row.get('Student_Name', f'Student {index}')),
                    'predicted_performance': 'Error',
                    'suggestions': [f'Error processing data: {str(e)}'],
                    'confidence': 0
                })
        
        # Commit all prediction records
        try:
            db.session.commit()
        except Exception as e:
            logging.error(f"Error committing batch predictions: {str(e)}")
            db.session.rollback()
        
        return jsonify({
            'results': results,
            'performance_stats': performance_stats,
            'total_students': len(results)
        })
        
    except Exception as e:
        logging.error(f"Error in predict_batch: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({'error': f'Batch prediction failed: {str(e)}'}), 500

@app.route('/presentation')
@login_required
def presentation():
    """Render presentation contents page"""
    return render_template('presentation.html', user=current_user)

@app.route('/full-presentation')
@login_required
def full_presentation():
    """Render full presentation with all diagrams"""
    from datetime import datetime
    return render_template('full_presentation.html', user=current_user, current_date=datetime.now().strftime('%B %d, %Y'))

@app.route('/api/model_info')
def model_info():
    """Get information about the ML model"""
    try:
        info = ml_model.get_model_info()
        return jsonify(info)
    except Exception as e:
        logging.error(f"Error getting model info: {str(e)}")
        return jsonify({'error': 'Failed to get model information'}), 500

@app.route('/api/sample_files')
def list_sample_files():
    """List available sample Excel files"""
    try:
        import os
        sample_dir = 'sample_data'
        if not os.path.exists(sample_dir):
            return jsonify({'files': []})
        
        files = [f for f in os.listdir(sample_dir) if f.endswith('.xlsx')]
        file_info = []
        
        for filename in files:
            filepath = os.path.join(sample_dir, filename)
            size = os.path.getsize(filepath)
            file_info.append({
                'filename': filename,
                'size': size,
                'download_url': url_for('download_sample_file', filename=filename)
            })
        
        return jsonify({'files': file_info})
    except Exception as e:
        logging.error(f"Error listing sample files: {str(e)}")
        return jsonify({'error': 'Failed to list sample files'}), 500

@app.route('/download/sample/<filename>')
def download_sample_file(filename):
    """Download a sample Excel file"""
    try:
        from flask import send_from_directory
        import os
        
        sample_dir = 'sample_data'
        
        # Security: only allow .xlsx files and prevent directory traversal
        if not filename.endswith('.xlsx') or '/' in filename or '\\' in filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        filepath = os.path.join(sample_dir, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(sample_dir, filename, as_attachment=True)
    except Exception as e:
        logging.error(f"Error downloading sample file: {str(e)}")
        return jsonify({'error': 'Failed to download file'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
