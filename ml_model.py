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
    
    def _generate_training_data(self, n_samples=5000):
        """Generate comprehensive synthetic training data for the model with realistic patterns"""
        np.random.seed(42)
        
        data = []
        
        for i in range(n_samples):
            # Create diverse student profiles with realistic patterns
            
            # Define different student archetypes for more realistic data - balanced distribution
            archetype = np.random.choice(['poor', 'average', 'good', 'excellent', 'inconsistent'], 
                                        p=[0.20, 0.30, 0.30, 0.15, 0.05])
            
            if archetype == 'poor':
                # Poor: Score < 45 (Grades < 60, Attendance < 70%, Study < 2 hrs/day)
                base_performance = np.random.uniform(0, 0.50)
                variance = 0.12
            elif archetype == 'average':
                # Average: Score 45-65 (Grades 60-74, Attendance 70-79%, Study 2-4 hrs/day)
                base_performance = np.random.uniform(0.50, 0.70)
                variance = 0.10
            elif archetype == 'good':
                # Good: Score 65-80 (Grades 75-84, Attendance 80-89%, Study 4-6 hrs/day)
                base_performance = np.random.uniform(0.70, 0.85)
                variance = 0.08
            elif archetype == 'excellent':
                # Excellent: Score > 80 (Grades 85-100, Attendance 90-100%, Study 6+ hrs/day)
                base_performance = np.random.uniform(0.85, 1.0)
                variance = 0.06
            else:  # inconsistent
                base_performance = np.random.uniform(0.30, 0.75)
                variance = 0.20
            
            # Previous grades with realistic distribution aligned to performance levels
            # Poor: <60, Average: 60-74, Good: 75-84, Excellent: 85-100
            if archetype == 'poor':
                previous_grades = np.clip(np.random.normal(50, 12), 0, 59)
            elif archetype == 'average':
                previous_grades = np.clip(np.random.normal(67, 7), 60, 74)
            elif archetype == 'good':
                previous_grades = np.clip(np.random.normal(79.5, 5), 75, 84)
            elif archetype == 'excellent':
                previous_grades = np.clip(np.random.normal(92, 5), 85, 100)
            else:  # inconsistent
                previous_grades = np.clip(np.random.normal(base_performance * 85 + 15, variance * 100), 0, 100)
            
            # Attendance aligned to performance levels
            # Poor: <70%, Average: 70-79%, Good: 80-89%, Excellent: 90-100%
            attendance_correlation = 0.85 if np.random.random() > 0.1 else 0.6
            if archetype == 'poor':
                attendance = np.clip(np.random.normal(60, 10), 0, 69) * attendance_correlation
            elif archetype == 'average':
                attendance = np.clip(np.random.normal(74.5, 5), 70, 79) * attendance_correlation
            elif archetype == 'good':
                attendance = np.clip(np.random.normal(84.5, 5), 80, 89) * attendance_correlation
            elif archetype == 'excellent':
                attendance = np.clip(np.random.normal(95, 5), 90, 100) * attendance_correlation
            else:  # inconsistent
                attendance = np.clip(np.random.normal(base_performance * 80 + 20, variance * 80) * attendance_correlation, 0, 100)
            
            # Study hours aligned to performance levels
            # Poor: <2 hrs/day, Average: 2-4 hrs/day, Good: 4-6 hrs/day, Excellent: 6+ hrs/day
            if archetype == 'poor':
                study_hours = np.clip(np.random.gamma(2, 0.8), 0, 2)
            elif archetype == 'average':
                study_hours = np.clip(np.random.normal(3, 0.7), 2, 4)
            elif archetype == 'good':
                study_hours = np.clip(np.random.normal(5, 0.7), 4, 6)
            elif archetype == 'excellent':
                study_hours = np.clip(np.random.gamma(3.5, 2), 6, 12)
            else:  # inconsistent
                base_study = base_performance * 7 + 1
                study_hours = np.clip(
                    np.random.gamma(base_study * 0.5, 2) if base_study > 3 else np.random.exponential(base_study),
                    0, 15
                )
            
            # Extracurricular activities - balanced distribution
            if base_performance > 0.7:
                extracurricular = np.random.choice([2, 3, 4, 5, 6], p=[0.1, 0.25, 0.35, 0.2, 0.1])
            elif base_performance > 0.4:
                extracurricular = np.random.choice([1, 2, 3, 4], p=[0.2, 0.4, 0.3, 0.1])
            else:
                extracurricular = np.random.choice([0, 1, 2, 3], p=[0.3, 0.4, 0.2, 0.1])
            
            # Interactiveness with realistic probability
            interactiveness_prob = base_performance * 0.7 + 0.15 + (np.random.random() * 0.1 - 0.05)
            interactiveness = 1 if np.random.random() < interactiveness_prob else 0
            
            # Practical knowledge with independent variation
            practical_score = base_performance + np.random.normal(0, 0.15)
            if practical_score < 0.20:
                practical_knowledge = 'Poor'
            elif practical_score < 0.45:
                practical_knowledge = 'Moderate'
            elif practical_score < 0.75:
                practical_knowledge = 'Good'
            else:
                practical_knowledge = 'Very Good'
            
            # Communication skill with independent variation
            comm_score = base_performance + np.random.normal(0, 0.18)
            if comm_score < 0.25:
                communication_skill = 'Poor'
            elif comm_score < 0.50:
                communication_skill = 'Moderate'
            elif comm_score < 0.75:
                communication_skill = 'Good'
            else:
                communication_skill = 'Very Good'
            
            # Projects handled - correlated with skills and time
            project_base = base_performance * 5 + 1
            projects = int(np.clip(
                np.random.poisson(project_base) + np.random.choice([-1, 0, 1], p=[0.1, 0.7, 0.2]),
                0, 15
            ))
            
            # Assignments completed - high correlation with discipline
            assignment_rate = base_performance * 0.85 + 0.10
            assignments = int(np.clip(
                np.random.binomial(20, assignment_rate),
                0, 20
            ))
            
            # Calculate performance with weighted combination and realistic thresholds
            # Encode categorical for calculation
            practical_encoded_val = {'Poor': 0, 'Moderate': 1, 'Good': 2, 'Very Good': 3}[practical_knowledge]
            comm_encoded_val = {'Poor': 0, 'Moderate': 1, 'Good': 2, 'Very Good': 3}[communication_skill]
            
            performance_score = (
                previous_grades * 0.35 +
                attendance * 0.20 +
                min(study_hours * 7.5, 60) * 0.15 +
                min(extracurricular * 3.5, 18) * 0.08 +
                interactiveness * 15 * 0.07 +
                practical_encoded_val * 7 * 0.08 +
                comm_encoded_val * 7 * 0.07
            )
            
            # Add random noise to make classification more realistic
            performance_score += np.random.normal(0, 2.5)
            
            # Determine performance category with realistic boundaries
            # Poor: < 45, Average: 45-65, Good: 65-80, Excellent: > 80
            if performance_score < 45:
                performance = 'Poor'
            elif performance_score < 65:
                performance = 'Average'
            elif performance_score <= 80:
                performance = 'Good'
            else:
                performance = 'Excellent'
            
            # Add edge cases and special scenarios (5% of data)
            if i % 20 == 0:
                # High grades but poor attendance
                if np.random.random() < 0.3:
                    attendance = np.random.uniform(40, 65)
                # High study hours but low grades (inefficient studying)
                elif np.random.random() < 0.3:
                    study_hours = np.random.uniform(8, 12)
                    previous_grades = np.random.uniform(50, 70)
                # Perfect attendance but struggling
                elif np.random.random() < 0.3:
                    attendance = np.random.uniform(95, 100)
                    previous_grades = np.random.uniform(40, 60)
            
            data.append({
                'Previous_Grades': round(previous_grades, 2),
                'Attendance_Percentage': round(attendance, 2),
                'Study_Hours_Per_Day': round(study_hours, 2),
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
