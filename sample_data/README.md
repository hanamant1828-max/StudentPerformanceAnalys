# Sample Excel Files for Student Performance Prediction

This folder contains sample Excel files that you can use to test the batch prediction feature of the Student Performance Prediction System.

## New Sample Files (Recommended)

### 1. **excellent_students_sample.xlsx** (5 students)
Contains data for 5 high-performing students:
- Grades: 88-95
- Attendance: 95-100%
- Study Hours: 7-9 hours/day
- Expected Prediction: **Excellent**

### 2. **good_students_sample.xlsx** (5 students)
Contains data for 5 good-performing students:
- Grades: 78-85
- Attendance: 85-90%
- Study Hours: 5.5-7 hours/day
- Expected Prediction: **Good**

### 3. **mixed_students_sample.xlsx** (10 students)
Contains 10 students with varied performance levels:
- Range from Poor to Excellent
- Good for testing different prediction outcomes
- Expected Predictions: Mixed (Poor, Average, Good, Excellent)

### 4. **large_class_30_students.xlsx** (30 students)
A complete class roster with diverse student profiles:
- 5 Excellent students
- 10 Good students
- 10 Average students
- 5 Poor students
- Perfect for testing bulk predictions

## Legacy Test Files

Additional smaller test files are also available:
- `test_data_excellent_students.xlsx`
- `test_data_good_students.xlsx`
- `test_data_average_students.xlsx`
- `test_data_poor_students.xlsx`
- `test_data_mixed_profiles.xlsx`
- `sample_students.xlsx`

## Required Excel Format

All Excel files must include these columns in this exact order:

1. **Student_Name** - Full name of the student
2. **Previous_Grades** - Numeric (0-100)
3. **Attendance_Percentage** - Numeric (0-100)
4. **Study_Hours_Per_Day** - Numeric (0-12)
5. **Extracurricular_Activities** - Integer (0-10)
6. **Interactiveness** - Text: "Yes" or "No"
7. **Practical_Knowledge** - Text: "Poor", "Moderate", "Good", or "Very Good"
8. **Communication_Skill** - Text: "Poor", "Moderate", "Good", or "Very Good"
9. **Projects_Handled** - Integer (0-20)
10. **Assignments_Completed** - Integer (0-20)

## How to Use

1. Log in to the Student Performance Prediction System
2. Navigate to the batch prediction section
3. Download any of these sample files
4. Upload the file to see batch predictions
5. Review the predicted performance for each student

## Performance Categories

The system predicts one of four performance levels:

- **Poor**: Overall score < 50
- **Average**: Overall score 50-70
- **Good**: Overall score 70-85
- **Excellent**: Overall score ≥ 85

## Download via API

You can also access these files programmatically:

- **List all files**: `GET /api/sample_files`
- **Download a file**: `GET /download/sample/{filename}`

Example: `/download/sample/excellent_students_sample.xlsx`

---

*Last updated: October 30, 2025*
