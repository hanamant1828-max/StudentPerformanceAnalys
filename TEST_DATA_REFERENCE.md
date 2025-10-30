
# Test Data Reference for Student Performance Prediction

## Quick Test Data Sets

### Excel Files Available
- `test_data_excellent_students.xlsx` - 4 excellent performers
- `test_data_good_students.xlsx` - 4 good performers
- `test_data_average_students.xlsx` - 4 average performers
- `test_data_poor_students.xlsx` - 4 poor performers
- `test_data_mixed_profiles.xlsx` - 8 students with varied performance levels

## Single Student Test Data (Copy-Paste Ready)

### Test Case 1: Excellent Student
```
Student Name: Alice Johnson
Previous Grades: 92
Attendance Percentage: 96
Study Hours Per Day: 7
Extracurricular Activities: 5
Interactiveness: yes
Practical Knowledge: Very Good
Communication Skill: Very Good
Projects Handled: 10
Assignments Completed: 20
```
**Expected Result:** Performance = Excellent, High Confidence (~85-95%)

---

### Test Case 2: Good Student
```
Student Name: David Wilson
Previous Grades: 82
Attendance Percentage: 88
Study Hours Per Day: 5.5
Extracurricular Activities: 4
Interactiveness: yes
Practical Knowledge: Good
Communication Skill: Good
Projects Handled: 9
Assignments Completed: 19
```
**Expected Result:** Performance = Good, Medium-High Confidence (~75-85%)

---

### Test Case 3: Average Student
```
Student Name: Carol Davis
Previous Grades: 68
Attendance Percentage: 78
Study Hours Per Day: 3.5
Extracurricular Activities: 2
Interactiveness: no
Practical Knowledge: Moderate
Communication Skill: Moderate
Projects Handled: 6
Assignments Completed: 15
```
**Expected Result:** Performance = Average, Medium Confidence (~65-75%)

---

### Test Case 4: Poor Student
```
Student Name: Bob Smith
Previous Grades: 48
Attendance Percentage: 62
Study Hours Per Day: 1.5
Extracurricular Activities: 0
Interactiveness: no
Practical Knowledge: Poor
Communication Skill: Poor
Projects Handled: 1
Assignments Completed: 9
```
**Expected Result:** Performance = Poor, Medium Confidence (~65-75%)

---

## Edge Case Test Data

### Test Case 5: High Grades, Low Attendance
```
Student Name: Smart but Absent
Previous Grades: 90
Attendance Percentage: 55
Study Hours Per Day: 6
Extracurricular Activities: 3
Interactiveness: no
Practical Knowledge: Good
Communication Skill: Good
Projects Handled: 8
Assignments Completed: 16
```
**Expected Suggestions:** Should include improving attendance

---

### Test Case 6: High Study Hours, Low Grades
```
Student Name: Hard Worker
Previous Grades: 55
Attendance Percentage: 85
Study Hours Per Day: 10
Extracurricular Activities: 2
Interactiveness: yes
Practical Knowledge: Moderate
Communication Skill: Moderate
Projects Handled: 5
Assignments Completed: 18
```
**Expected Suggestions:** Should include improving study effectiveness

---

### Test Case 7: Perfect Attendance, Struggling
```
Student Name: Always Present
Previous Grades: 50
Attendance Percentage: 100
Study Hours Per Day: 2
Extracurricular Activities: 1
Interactiveness: no
Practical Knowledge: Poor
Communication Skill: Poor
Projects Handled: 3
Assignments Completed: 10
```
**Expected Suggestions:** Should include increasing study hours and engagement

---

## Field Validation Test Data

### Test Case 8: Minimum Values
```
Student Name: Min Values Test
Previous Grades: 0
Attendance Percentage: 0
Study Hours Per Day: 0
Extracurricular Activities: 0
Interactiveness: no
Practical Knowledge: Poor
Communication Skill: Poor
Projects Handled: 0
Assignments Completed: 0
```
**Expected Result:** Should accept and process without errors

---

### Test Case 9: Maximum Values
```
Student Name: Max Values Test
Previous Grades: 100
Attendance Percentage: 100
Study Hours Per Day: 15
Extracurricular Activities: 10
Interactiveness: yes
Practical Knowledge: Very Good
Communication Skill: Very Good
Projects Handled: 20
Assignments Completed: 25
```
**Expected Result:** Should accept and process without errors

---

## Field Reference

### Required Fields and Valid Ranges

| Field Name | Type | Valid Range/Values | Example |
|------------|------|-------------------|---------|
| Student Name | Text | Any text | "John Doe" |
| Previous Grades | Number | 0-100 | 85 |
| Attendance Percentage | Number | 0-100 | 90 |
| Study Hours Per Day | Number | 0-24 | 5.5 |
| Extracurricular Activities | Number | 0+ | 3 |
| Interactiveness | Text | "yes" or "no" | yes |
| Practical Knowledge | Text | Poor, Moderate, Good, Very Good | Good |
| Communication Skill | Text | Poor, Moderate, Good, Very Good | Very Good |
| Projects Handled | Number | 0+ | 8 |
| Assignments Completed | Number | 0+ | 18 |

---

## Quick Testing Workflow

### For Single Student Prediction:
1. Login with demo account (username: `demo`, password: `demo123`)
2. Navigate to "Single Student" tab
3. Copy any test case data from above
4. Paste into form fields
5. Click "Predict Performance"
6. Verify results match expected performance category

### For Batch Prediction:
1. Login with demo account
2. Navigate to "Batch Upload" tab
3. Download any of the pre-created Excel files
4. Upload the file
5. Click "Upload and Predict"
6. Verify all students are processed
7. Check performance statistics distribution

---

## Common Test Scenarios

### Scenario 1: New User Registration and First Prediction
1. Register new account
2. Make a single prediction using Test Case 1
3. View dashboard to see prediction saved

### Scenario 2: Batch Processing
1. Upload `test_data_mixed_profiles.xlsx`
2. Verify all 8 students are processed
3. Check performance distribution shows variety

### Scenario 3: History Tracking
1. Make 5+ predictions (mix of single and batch)
2. Navigate to dashboard
3. Verify recent predictions table shows all entries
4. Check statistics are calculated correctly

---

## Error Testing

### Invalid File Upload
- Try uploading .txt, .pdf, .jpg files (should be rejected)
- Upload empty Excel file (should handle gracefully)
- Upload Excel with wrong column names (should show error)

### Invalid Input Values
- Grades > 100 (should be blocked by UI)
- Attendance < 0 (should be blocked by UI)
- Empty required fields (should show validation error)

---

## Performance Categories Reference

| Category | Typical Characteristics |
|----------|------------------------|
| **Excellent** | Grades: 85-100, Attendance: 90-100%, Study: 6+ hrs, High engagement |
| **Good** | Grades: 75-84, Attendance: 80-89%, Study: 4-6 hrs, Good engagement |
| **Average** | Grades: 60-74, Attendance: 70-79%, Study: 2-4 hrs, Moderate engagement |
| **Poor** | Grades: <60, Attendance: <70%, Study: <2 hrs, Low engagement |

---

## Notes
- All test data is synthetic and generated for testing purposes
- Confidence scores typically range from 65% to 95%
- The system provides personalized suggestions based on performance category
- All predictions are saved to user history with timestamps
