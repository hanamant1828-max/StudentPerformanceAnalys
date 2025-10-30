
# Student Performance Prediction System - Test Cases

## 1. Authentication Test Cases

### 1.1 User Registration Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| REG-001 | Valid registration with all fields | username: "testuser1", email: "test1@example.com", password: "test123", first_name: "Test", last_name: "User", role: "student" | User created successfully, auto-login, redirect to index |
| REG-002 | Registration with existing username | username: "demo" (existing), email: "newuser@example.com", password: "test123" | Error: "Username already exists" |
| REG-003 | Registration with existing email | username: "newuser", email: "demo@example.com" (existing), password: "test123" | Error: "Email already registered" |
| REG-004 | Registration with short password | password: "12345" (less than 6 chars) | Error: "Password must be at least 6 characters long" |
| REG-005 | Registration with mismatched passwords | password: "test123", confirm_password: "test456" | Error: "Passwords do not match" |
| REG-006 | Registration with invalid email | email: "invalid-email" | Error: "Invalid email address" |
| REG-007 | Registration with missing required fields | first_name: "" | Error: "First name is required" |
| REG-008 | Registration with different roles | role: "teacher" / "admin" | User created with specified role |

### 1.2 User Login Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| LOG-001 | Valid login with username | username: "demo", password: "demo123" | Login successful, redirect to index |
| LOG-002 | Valid login with email | username: "demo@example.com", password: "demo123" | Login successful, redirect to index |
| LOG-003 | Invalid username | username: "nonexistent", password: "demo123" | Error: "Invalid username or password" |
| LOG-004 | Invalid password | username: "demo", password: "wrongpass" | Error: "Invalid username or password" |
| LOG-005 | Login with deactivated account | Create deactivated user, attempt login | Error: "Your account has been deactivated" |
| LOG-006 | Remember me functionality | Check "remember me" checkbox | Session persists after browser restart |
| LOG-007 | Login with empty credentials | username: "", password: "" | Error: "Please provide both username and password" |

### 1.3 User Logout Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| LOGOUT-001 | Logout from authenticated session | Click logout | User logged out, redirect to login page |
| LOGOUT-002 | Access protected pages after logout | Navigate to /dashboard after logout | Redirect to login page |

## 2. Single Student Prediction Test Cases

### 2.1 Valid Prediction Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| PRED-001 | Excellent student prediction | previous_grades: 95, attendance: 98, study_hours: 8, extracurricular: 5, interactiveness: "yes", practical_knowledge: "Very Good", communication_skill: "Very Good", projects: 12, assignments: 20 | Performance: "Excellent", High confidence |
| PRED-002 | Good student prediction | previous_grades: 80, attendance: 85, study_hours: 5, extracurricular: 3, interactiveness: "yes", practical_knowledge: "Good", communication_skill: "Good", projects: 8, assignments: 18 | Performance: "Good", Medium-High confidence |
| PRED-003 | Average student prediction | previous_grades: 65, attendance: 75, study_hours: 3, extracurricular: 2, interactiveness: "no", practical_knowledge: "Moderate", communication_skill: "Moderate", projects: 5, assignments: 14 | Performance: "Average", Medium confidence |
| PRED-004 | Poor student prediction | previous_grades: 45, attendance: 60, study_hours: 1, extracurricular: 1, interactiveness: "no", practical_knowledge: "Poor", communication_skill: "Poor", projects: 2, assignments: 8 | Performance: "Poor", Medium confidence |

### 2.2 Edge Case Predictions
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| PRED-005 | Minimum values | All numeric fields: 0 or minimum | Prediction completes successfully |
| PRED-006 | Maximum values | previous_grades: 100, attendance: 100, study_hours: 15, etc. | Prediction completes successfully |
| PRED-007 | High grades but low attendance | previous_grades: 90, attendance: 55, other fields moderate | Suggestions include improving attendance |
| PRED-008 | High study hours but low grades | study_hours: 10, previous_grades: 55, other fields moderate | Suggestions include study effectiveness |
| PRED-009 | Perfect attendance but struggling | attendance: 100, previous_grades: 50, other fields low | Prediction shows need for other improvements |

### 2.3 Input Validation Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| PRED-010 | Missing required field | student_name: "" | Error: "Missing required field: student_name" |
| PRED-011 | Invalid grade value | previous_grades: 150 (out of range) | UI validation prevents submission |
| PRED-012 | Invalid attendance value | attendance: -10 or 110 | UI validation prevents submission |
| PRED-013 | Invalid study hours | study_hours: -5 or 25 | UI validation prevents submission |
| PRED-014 | Non-numeric input in numeric field | previous_grades: "abc" | Error or validation prevents submission |
| PRED-015 | Valid student name formats | student_name: "John Doe", "María García", "李明" | Name saved correctly |

## 3. Batch Prediction Test Cases

### 3.1 Valid Batch Upload Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| BATCH-001 | Upload valid Excel file with 5 students | sample_students.xlsx (provided) | All 5 predictions successful, statistics shown |
| BATCH-002 | Upload file with 1 student | Excel with single row | Single prediction successful |
| BATCH-003 | Upload file with 100+ students | Excel with 100 rows | All predictions successful, performance stats calculated |
| BATCH-004 | Upload file with diverse data | Mix of excellent, good, average, poor students | Accurate predictions for all categories |

### 3.2 Invalid Batch Upload Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| BATCH-005 | Upload non-Excel file | .txt, .pdf, .jpg file | Error: "Invalid file format. Please upload Excel file" |
| BATCH-006 | Upload empty file | Empty Excel file | Error or empty results |
| BATCH-007 | Upload file with missing columns | Excel missing "Student_Name" column | Error: "Missing columns in Excel file: Student_Name" |
| BATCH-008 | Upload file with incorrect column names | Misspelled column names | Error listing missing columns |
| BATCH-009 | Upload file with invalid data types | String values in numeric columns | Error processing specific rows |
| BATCH-010 | Upload file with special characters | Names with emojis, symbols | Should handle gracefully |
| BATCH-011 | No file selected | Click submit without selecting file | Error: "No file selected" |

### 3.3 Batch Results Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| BATCH-012 | Verify performance statistics | Upload known distribution | Stats match actual predictions |
| BATCH-013 | Download results | After batch prediction | Results downloadable as Excel |
| BATCH-014 | View individual student details | Click on student in results | Full prediction details displayed |

## 4. Dashboard Test Cases

### 4.1 Statistics Display Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| DASH-001 | View dashboard with no predictions | New user account | Shows 0 predictions, empty state messages |
| DASH-002 | View dashboard with predictions | User with 10+ predictions | Statistics display correctly |
| DASH-003 | Total predictions count | After making predictions | Count matches actual predictions made |
| DASH-004 | Average confidence calculation | Mix of predictions | Average calculated correctly |
| DASH-005 | Batch vs single count | Make both types | Counts separated correctly |

### 4.2 Performance Distribution Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| DASH-006 | Pie chart display | User with varied predictions | Chart shows correct distribution |
| DASH-007 | Performance breakdown bars | User with predictions | Progress bars show correct percentages |
| DASH-008 | All one category | All predictions are "Excellent" | Chart and bars reflect 100% in one category |

### 4.3 Recent Predictions Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| DASH-009 | Recent predictions table | User with 15+ predictions | Shows 10 most recent |
| DASH-010 | Table sorting | Click column headers | Table sorts correctly |
| DASH-011 | Table pagination | User with 20+ predictions | Pagination works (5 per page) |
| DASH-012 | Prediction type badges | Mix of batch and single | Badges display correctly |

## 5. UI/UX Test Cases

### 5.1 Navigation Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| NAV-001 | Navigate between tabs | Click Single/Batch/Results tabs | Tabs switch correctly |
| NAV-002 | Navigate to dashboard | Click "View Dashboard" button | Dashboard loads |
| NAV-003 | User dropdown menu | Click user icon | Menu shows with correct options |
| NAV-004 | Quick action buttons | Click buttons on dashboard | Navigate to correct pages |

### 5.2 Form Interaction Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| FORM-001 | Form field validation | Enter invalid values | Real-time validation feedback |
| FORM-002 | Form reset | Submit form, then reset | All fields cleared |
| FORM-003 | Dropdown selections | Select different options | Values update correctly |
| FORM-004 | File upload interface | Drag and drop file | File selected successfully |

### 5.3 Responsive Design Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| RESP-001 | Mobile view (320px-768px) | View on mobile device | Layout adapts, all functions work |
| RESP-002 | Tablet view (768px-1024px) | View on tablet | Layout adapts appropriately |
| RESP-003 | Desktop view (1024px+) | View on desktop | Full layout displays correctly |

## 6. Data Persistence Test Cases

### 6.1 Database Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| DB-001 | Prediction saved to history | Make single prediction | Prediction appears in dashboard |
| DB-002 | User data persistence | Register, logout, login | User data retained |
| DB-003 | Prediction history after logout | Make predictions, logout, login | History persists |
| DB-004 | Concurrent users | Multiple users making predictions | Data isolated per user |

## 7. Performance Test Cases

### 7.1 Load Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| PERF-001 | Single prediction response time | Standard input | Response < 2 seconds |
| PERF-002 | Batch prediction (10 students) | Excel with 10 rows | Processing < 5 seconds |
| PERF-003 | Batch prediction (100 students) | Excel with 100 rows | Processing < 30 seconds |
| PERF-004 | Large file upload | Excel with 1000+ rows | Handles gracefully or shows appropriate message |

## 8. Security Test Cases

### 8.1 Authentication Security Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| SEC-001 | Access protected endpoint without login | Direct URL to /api/predict_single | Redirect to login or 401 error |
| SEC-002 | SQL injection attempt | username: "' OR '1'='1" | Input sanitized, login fails safely |
| SEC-003 | XSS attempt in student name | student_name: "<script>alert('xss')</script>" | Input escaped, no script execution |
| SEC-004 | Password hashing | Check database | Passwords stored as hashes, not plaintext |
| SEC-005 | Session hijacking prevention | Attempt to use another user's session | Access denied |

## 9. ML Model Test Cases

### 9.1 Model Accuracy Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| ML-001 | Model training completion | App startup | Model trains with ~90% accuracy |
| ML-002 | Prediction consistency | Same input multiple times | Same prediction each time |
| ML-003 | Confidence score range | Various inputs | Confidence between 0 and 1 |
| ML-004 | Suggestion generation | Each performance category | Relevant suggestions provided |

## 10. Error Handling Test Cases

### 10.1 System Error Tests
| Test Case ID | Description | Test Data | Expected Result |
|-------------|-------------|-----------|-----------------|
| ERR-001 | Database connection failure | Simulate DB error | Graceful error message, app doesn't crash |
| ERR-002 | Invalid API request | Malformed JSON | 400 error with clear message |
| ERR-003 | Server error | Force 500 error | User-friendly error page |
| ERR-004 | Network timeout | Slow connection simulation | Appropriate timeout handling |

## Test Execution Priority

**Priority 1 (Critical):**
- REG-001 to REG-007 (Registration)
- LOG-001 to LOG-007 (Login)
- PRED-001 to PRED-004 (Basic Predictions)
- BATCH-001, BATCH-005 to BATCH-008 (Batch Upload)

**Priority 2 (High):**
- PRED-005 to PRED-015 (Edge Cases & Validation)
- DASH-001 to DASH-012 (Dashboard)
- DB-001 to DB-004 (Data Persistence)
- SEC-001 to SEC-005 (Security)

**Priority 3 (Medium):**
- NAV-001 to FORM-004 (UI/UX)
- BATCH-009 to BATCH-014 (Advanced Batch)
- PERF-001 to PERF-004 (Performance)
- ML-001 to ML-004 (ML Model)

**Priority 4 (Low):**
- RESP-001 to RESP-003 (Responsive Design)
- ERR-001 to ERR-004 (Error Handling)

## Sample Test Data

### Sample Student 1 (Excellent)
```
Student_Name: Alice Johnson
Previous_Grades: 92
Attendance_Percentage: 96
Study_Hours_Per_Day: 7
Extracurricular_Activities: 5
Interactiveness: yes
Practical_Knowledge: Very Good
Communication_Skill: Very Good
Projects_Handled: 10
Assignments_Completed: 20
```

### Sample Student 2 (Poor)
```
Student_Name: Bob Smith
Previous_Grades: 48
Attendance_Percentage: 62
Study_Hours_Per_Day: 1.5
Extracurricular_Activities: 0
Interactiveness: no
Practical_Knowledge: Poor
Communication_Skill: Poor
Projects_Handled: 1
Assignments_Completed: 9
```

### Sample Student 3 (Average)
```
Student_Name: Carol Davis
Previous_Grades: 68
Attendance_Percentage: 78
Study_Hours_Per_Day: 3.5
Extracurricular_Activities: 2
Interactiveness: no
Practical_Knowledge: Moderate
Communication_Skill: Moderate
Projects_Handled: 6
Assignments_Completed: 15
```

### Sample Student 4 (Good)
```
Student_Name: David Wilson
Previous_Grades: 82
Attendance_Percentage: 88
Study_Hours_Per_Day: 5.5
Extracurricular_Activities: 4
Interactiveness: yes
Practical_Knowledge: Good
Communication_Skill: Good
Projects_Handled: 9
Assignments_Completed: 19
```
