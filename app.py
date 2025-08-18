import os
import logging
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from ml_model import StudentPerformanceModel
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Enable CORS
CORS(app)

# Initialize ML model
ml_model = StudentPerformanceModel()

@app.route('/')
def index():
    """Render the main application page"""
    return render_template('index.html')

@app.route('/api/predict_single', methods=['POST'])
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
        
        result = {
            'student_name': data['student_name'],
            'predicted_performance': prediction,
            'suggestions': suggestions,
            'confidence': ml_model.get_prediction_confidence(student_data)
        }
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Error in predict_single: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/api/predict_batch', methods=['POST'])
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
                performance_stats[prediction] += 1
                
                results.append({
                    'student_name': str(row['Student_Name']),
                    'predicted_performance': prediction,
                    'suggestions': suggestions,
                    'confidence': ml_model.get_prediction_confidence(student_data)
                })
                
            except Exception as e:
                logging.error(f"Error processing row {index}: {str(e)}")
                results.append({
                    'student_name': str(row.get('Student_Name', f'Student {index}')),
                    'predicted_performance': 'Error',
                    'suggestions': [f'Error processing data: {str(e)}'],
                    'confidence': 0
                })
        
        return jsonify({
            'results': results,
            'performance_stats': performance_stats,
            'total_students': len(results)
        })
        
    except Exception as e:
        logging.error(f"Error in predict_batch: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({'error': f'Batch prediction failed: {str(e)}'}), 500

@app.route('/api/model_info')
def model_info():
    """Get information about the ML model"""
    try:
        info = ml_model.get_model_info()
        return jsonify(info)
    except Exception as e:
        logging.error(f"Error getting model info: {str(e)}")
        return jsonify({'error': 'Failed to get model information'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
