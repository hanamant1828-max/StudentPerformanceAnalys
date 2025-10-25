# Overview

This is a Student Performance Prediction System with user authentication that uses machine learning to predict academic performance based on various student factors. The application provides user registration/login, single student prediction and batch processing capabilities through Excel file uploads. It classifies students into performance categories (Poor, Average, Good, Excellent) and provides personalized improvement suggestions with interactive data visualizations. All predictions are saved to user history with SQLite database.

# Recent Changes

**October 25, 2025**
- Enhanced ML training data from 1,000 to 5,000 samples for improved accuracy
- Implemented 5 student archetypes for more realistic predictions
- Added edge cases (5%) to handle special scenarios
- Improved feature correlations with realistic statistical distributions
- Maintained model accuracy at ~91%
- Added "View Dashboard" button on main page for easier navigation

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Technology Stack**: HTML5, CSS3, JavaScript with jQuery
- **UI Framework**: Bootstrap 5 with dark theme for responsive design
- **Data Visualization**: Chart.js for interactive pie charts showing performance distribution
- **Table Management**: DataTables for sortable and searchable results display
- **Communication**: AJAX for asynchronous backend communication
- **File Handling**: SheetJS (xlsx) library for Excel file processing

## Backend Architecture
- **Framework**: Flask (Python) with CORS enabled for cross-origin requests
- **Authentication**: Flask-Login with user registration and login system
- **Database**: SQLite with SQLAlchemy ORM for user management and prediction history
- **Application Structure**: Modular Flask application with separate models and ML component
- **Request Handling**: Protected RESTful API endpoints for single and batch predictions
- **Error Handling**: Comprehensive try-catch blocks with proper HTTP status codes
- **Deployment**: ProxyFix middleware for reverse proxy compatibility

## Machine Learning Component
- **Algorithm**: Random Forest Classifier with 100 estimators
- **Training Dataset**: 5,000 synthetic student records with realistic patterns
- **Model Accuracy**: ~91% on test set
- **Data Processing**: Pandas for data manipulation and preprocessing
- **Feature Engineering**: Label encoders for categorical variables
- **Training Strategy**: Advanced synthetic data with 5 student archetypes (struggling, average, good, excellent, inconsistent)
- **Performance Metrics**: Accuracy tracking and classification reporting
- **Model Persistence**: Pickle serialization capability for model saving/loading
- **Data Diversity**: Includes edge cases and special scenarios for robust predictions

## Data Architecture
- **Database**: SQLite with user management and prediction history tables
- **User Management**: User authentication with roles (student, teacher, admin)
- **Input Features**: 10 student attributes including grades, attendance, study habits, and skills
- **Feature Types**: Mix of numerical (grades, hours) and categorical (skills, activities) data
- **Performance Categories**: 4-level classification system (Poor/Average/Good/Excellent)
- **Data Validation**: Required field validation and type checking
- **Batch Processing**: Excel file upload support with structured column mapping
- **Prediction History**: All predictions saved with user association and timestamps

## Frontend-Backend Integration
- **API Endpoints**: RESTful design with `/api/predict_single` and batch prediction routes
- **Data Flow**: JSON-based communication between frontend and backend
- **User Interface**: Tabbed interface for different prediction modes
- **Results Display**: Real-time updates with visual feedback and loading states

# External Dependencies

## Python Libraries
- **Flask**: Web framework for backend API development
- **Flask-Login**: User session management and authentication
- **Flask-SQLAlchemy**: Database ORM for SQLite
- **Flask-CORS**: Cross-origin resource sharing support
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing support
- **Scikit-learn**: Machine learning algorithms and utilities
- **Werkzeug**: WSGI utilities and proxy fix middleware
- **Email-Validator**: Email validation for registration

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design
- **jQuery**: JavaScript library for DOM manipulation
- **Chart.js**: Data visualization library for charts
- **DataTables**: Enhanced table functionality
- **Font Awesome**: Icon library for UI enhancement
- **SheetJS**: Excel file processing capability

## CDN Dependencies
- Bootstrap CSS and JS from CDN
- DataTables styling and functionality
- Font Awesome icons
- Chart.js visualization library

## Infrastructure Requirements
- **Python 3.6+**: Runtime environment
- **Web Server**: Flask development server (production-ready alternatives recommended)
- **Browser Compatibility**: Modern browsers with JavaScript support
- **Memory**: Minimum 4GB RAM for optimal performance