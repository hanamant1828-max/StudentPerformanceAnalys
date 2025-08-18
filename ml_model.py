import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import logging
import pickle
import os

class StudentPerformanceModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoders = {}
        self.feature_columns = [
            'Previous_Grades', 'Attendance_Percentage', 'Study_Hours_Per_Day',
            'Extracurricular_Activities', 'Interactiveness', 'Practical_Knowledge_Encoded',
            'Communication_Skill_Encoded', 'Projects_Handled', 'Assignments_Completed'
        ]
        self.performance_categories = ['Poor', 'Average', 'Good', 'Excellent']
        self.is_trained = False
        self.accuracy = 0.0
        
        # Initialize and train the model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the model with synthetic training data"""
        try:
            # Generate synthetic training data
            training_data = self._generate_training_data()
            
            # Train the model
            self._train_model(training_data)
            
            logging.info("Model initialized and trained successfully")
            
        except Exception as e:
            logging.error(f"Error initializing model: {str(e)}")
            raise
    
    def _generate_training_data(self, n_samples=1000):
        """Generate synthetic training data for the model"""
        np.random.seed(42)
        
        data = []
        
        for _ in range(n_samples):
            # Generate correlated features that make sense for student performance
            
            # Base performance level (hidden variable that influences all features)
            base_performance = np.random.uniform(0, 1)
            
            # Previous grades (strongly correlated with performance)
            previous_grades = np.clip(
                np.random.normal(base_performance * 90 + 10, 15), 0, 100
            )
            
            # Attendance (correlated with performance)
            attendance = np.clip(
                np.random.normal(base_performance * 85 + 15, 10), 0, 100
            )
            
            # Study hours (somewhat correlated)
            study_hours = np.clip(
                np.random.normal(base_performance * 6 + 2, 2), 0, 12
            )
            
            # Extracurricular activities
            extracurricular = np.random.poisson(base_performance * 3 + 1)
            
            # Interactiveness (binary)
            interactiveness = 1 if np.random.random() < (base_performance * 0.6 + 0.2) else 0
            
            # Practical knowledge (categorical)
            practical_prob = base_performance * 0.7 + 0.1
            if practical_prob < 0.25:
                practical_knowledge = 'Poor'
            elif practical_prob < 0.5:
                practical_knowledge = 'Moderate'
            elif practical_prob < 0.75:
                practical_knowledge = 'Good'
            else:
                practical_knowledge = 'Very Good'
            
            # Communication skill (categorical)
            comm_prob = base_performance * 0.7 + 0.1
            if comm_prob < 0.25:
                communication_skill = 'Poor'
            elif comm_prob < 0.5:
                communication_skill = 'Moderate'
            elif comm_prob < 0.75:
                communication_skill = 'Good'
            else:
                communication_skill = 'Very Good'
            
            # Projects handled
            projects = np.random.poisson(base_performance * 4 + 1)
            
            # Assignments completed
            assignments = np.clip(
                np.random.normal(base_performance * 18 + 2, 3), 0, 20
            )
            
            # Determine performance category based on weighted combination
            performance_score = (
                previous_grades * 0.3 +
                attendance * 0.2 +
                study_hours * 5 * 0.15 +
                extracurricular * 5 * 0.1 +
                interactiveness * 20 * 0.1 +
                (practical_prob * 100) * 0.075 +
                (comm_prob * 100) * 0.075
            )
            
            if performance_score < 40:
                performance = 'Poor'
            elif performance_score < 60:
                performance = 'Average'
            elif performance_score < 80:
                performance = 'Good'
            else:
                performance = 'Excellent'
            
            data.append({
                'Previous_Grades': previous_grades,
                'Attendance_Percentage': attendance,
                'Study_Hours_Per_Day': study_hours,
                'Extracurricular_Activities': extracurricular,
                'Interactiveness': interactiveness,
                'Practical_Knowledge': practical_knowledge,
                'Communication_Skill': communication_skill,
                'Projects_Handled': projects,
                'Assignments_Completed': assignments,
                'Performance': performance
            })
        
        return pd.DataFrame(data)
    
    def _train_model(self, data):
        """Train the RandomForest model"""
        # Encode categorical variables
        self.label_encoders['Practical_Knowledge'] = LabelEncoder()
        self.label_encoders['Communication_Skill'] = LabelEncoder()
        
        data['Practical_Knowledge_Encoded'] = self.label_encoders['Practical_Knowledge'].fit_transform(
            data['Practical_Knowledge']
        )
        data['Communication_Skill_Encoded'] = self.label_encoders['Communication_Skill'].fit_transform(
            data['Communication_Skill']
        )
        
        # Prepare features and target
        X = data[self.feature_columns]
        y = data['Performance']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        
        self.is_trained = True
        
        logging.info(f"Model trained with accuracy: {self.accuracy:.2f}")
        logging.info(f"Classification report:\n{classification_report(y_test, y_pred)}")
    
    def _prepare_features(self, student_data):
        """Prepare student data for prediction"""
        # Encode categorical variables
        practical_encoded = self.label_encoders['Practical_Knowledge'].transform([student_data['Practical_Knowledge']])[0]
        communication_encoded = self.label_encoders['Communication_Skill'].transform([student_data['Communication_Skill']])[0]
        
        features = [
            student_data['Previous_Grades'],
            student_data['Attendance_Percentage'],
            student_data['Study_Hours_Per_Day'],
            student_data['Extracurricular_Activities'],
            student_data['Interactiveness'],
            practical_encoded,
            communication_encoded,
            student_data['Projects_Handled'],
            student_data['Assignments_Completed']
        ]
        
        return np.array(features).reshape(1, -1)
    
    def predict_single(self, student_data):
        """Predict performance for a single student"""
        if not self.is_trained:
            raise Exception("Model is not trained")
        
        try:
            # Prepare features
            features = self._prepare_features(student_data)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            # Generate suggestions
            suggestions = self._generate_suggestions(student_data, prediction)
            
            return prediction, suggestions
            
        except Exception as e:
            logging.error(f"Error in prediction: {str(e)}")
            raise
    
    def get_prediction_confidence(self, student_data):
        """Get prediction confidence (probability of predicted class)"""
        if not self.is_trained:
            return 0.0
        
        try:
            features = self._prepare_features(student_data)
            probabilities = self.model.predict_proba(features)[0]
            return float(np.max(probabilities))
        except:
            return 0.0
    
    def _generate_suggestions(self, student_data, prediction):
        """Generate personalized suggestions based on student data and prediction"""
        suggestions = []
        
        # Analyze each factor and provide specific suggestions
        
        # Previous Grades
        if student_data['Previous_Grades'] < 60:
            suggestions.append("Focus on improving foundational knowledge in weak subjects")
            suggestions.append("Consider getting tutoring or joining study groups")
        elif student_data['Previous_Grades'] < 80:
            suggestions.append("Review and strengthen concepts in subjects with lower grades")
        
        # Attendance
        if student_data['Attendance_Percentage'] < 75:
            suggestions.append("Improve class attendance - aim for at least 85% attendance")
            suggestions.append("Catch up on missed lectures through recordings or notes")
        elif student_data['Attendance_Percentage'] < 85:
            suggestions.append("Maintain consistent attendance to stay engaged with coursework")
        
        # Study Hours
        if student_data['Study_Hours_Per_Day'] < 3:
            suggestions.append("Increase daily study time to at least 3-4 hours")
            suggestions.append("Create a structured study schedule and stick to it")
        elif student_data['Study_Hours_Per_Day'] < 5:
            suggestions.append("Optimize study time with focused, distraction-free sessions")
        
        # Extracurricular Activities
        if student_data['Extracurricular_Activities'] < 2:
            suggestions.append("Participate in more extracurricular activities to develop well-rounded skills")
        elif student_data['Extracurricular_Activities'] > 5:
            suggestions.append("Balance extracurricular activities with academic commitments")
        
        # Interactiveness
        if student_data['Interactiveness'] == 0:
            suggestions.append("Increase participation in class discussions and Q&A sessions")
            suggestions.append("Ask questions when concepts are unclear")
        
        # Practical Knowledge
        if student_data['Practical_Knowledge'] in ['Poor', 'Moderate']:
            suggestions.append("Focus on hands-on practice and practical applications")
            suggestions.append("Seek internships or project-based learning opportunities")
        
        # Communication Skills
        if student_data['Communication_Skill'] in ['Poor', 'Moderate']:
            suggestions.append("Work on improving communication skills through presentations and group work")
            suggestions.append("Consider joining debate clubs or public speaking groups")
        
        # Projects
        if student_data['Projects_Handled'] < 3:
            suggestions.append("Take on more project work to gain practical experience")
            suggestions.append("Collaborate on group projects to learn teamwork skills")
        
        # Assignments
        if student_data['Assignments_Completed'] < 15:
            suggestions.append("Complete all assigned work on time")
            suggestions.append("Use assignment feedback to improve future submissions")
        
        # Performance-specific suggestions
        if prediction == 'Poor':
            suggestions.append("Consider meeting with academic advisors for personalized support")
            suggestions.append("Explore additional resources like learning centers or peer tutoring")
        elif prediction == 'Average':
            suggestions.append("Focus on consistency in all areas to move to the next level")
            suggestions.append("Identify your strongest subjects and leverage them")
        elif prediction == 'Good':
            suggestions.append("Push yourself with advanced coursework or leadership roles")
            suggestions.append("Mentor struggling students to reinforce your own learning")
        else:  # Excellent
            suggestions.append("Continue your excellent work and consider research opportunities")
            suggestions.append("Share your study strategies with peers")
        
        # Remove duplicates and limit to most relevant suggestions
        unique_suggestions = list(dict.fromkeys(suggestions))
        return unique_suggestions[:8]  # Return top 8 suggestions
    
    def get_model_info(self):
        """Get information about the trained model"""
        return {
            'model_type': 'Random Forest Classifier',
            'is_trained': self.is_trained,
            'accuracy': round(self.accuracy, 3),
            'features': self.feature_columns,
            'performance_categories': self.performance_categories,
            'n_estimators': self.model.n_estimators if self.is_trained else 0
        }
