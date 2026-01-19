# Quiz Platform - Django MPA Project

A fully functional quiz platform built with Django, implementing a Multi-Page Application (MPA) architecture with templates. This project conforms to the course requirements for *Techniki Internetowe*.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Test Accounts](#test-accounts)
- [Development](#development)
- [Standards Compliance](#standards-compliance)

## ✨ Features

### User Roles & Authentication
- **Two-tier authorization system:**
  - **Students:** Take quizzes, view results, track history, and see leaderboards
  - **Teachers:** Create/edit quizzes, manage questions, view reports and analytics
- Session-based authentication with Django's built-in auth system
- User registration with role selection
- Profile management with avatar support

### Quiz Management (Teachers)
- Create and edit quizzes with various settings:
  - Categories, difficulty levels, time limits
  - Passing scores, maximum attempts
  - Question randomization, answer display settings
- Multiple question types:
  - Single choice
  - Multiple choice
  - True/False
  - Short answer (text)
- Add explanations and images to questions
- View detailed reports and analytics

### Taking Quizzes (Students)
- Browse available quizzes with filtering and search
- Real-time timer for timed quizzes
- Auto-save progress (localStorage)
- Immediate feedback on completion
- View detailed results with explanations
- Track quiz history and performance

### Additional Features
- Leaderboards (per quiz and overall)
- Dashboard with statistics for both roles
- Responsive design with Bootstrap 5
- W3C HTML5 compliant
- Interactive features with vanilla JavaScript

## 🛠 Technology Stack

- **Backend:** Django 6.0+ (Python 3.12+)
- **Database:** SQLite (development)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **CSS Framework:** Bootstrap 5.3
- **Icons:** Font Awesome 6.4
- **Architecture:** MPA (Multi-Page Application) with Django templates
- **Package Management:** uv (recommended) or pip

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12 or newer
- uv package manager (recommended) or pip
- Git

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd techniki-internetowe
   ```

2. **Install dependencies:**
   ```bash
   # Using uv (recommended)
   uv pip install -e .
   
   # Or using pip
   pip install -e .
   ```

3. **Install development dependencies (optional):**
   ```bash
   uv pip install -e ".[dev]"
   ```

4. **Run database migrations:**
   ```bash
   uv run python manage.py migrate
   ```

5. **Load sample data:**
   ```bash
   uv run python manage.py load_sample_data
   ```
   
   This command creates:
   - Sample categories (Python, JavaScript, Databases, Web Development)
   - Test users (teacher and student)
   - Sample quizzes with questions
   - Sample results

6. **Create a superuser (optional):**
   ```bash
   uv run python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   # Directly
   uv run python manage.py runserver
   
   # Or using the helper script
   ./utils/run_django.sh
   ```

8. **Access the application:**
   - Homepage: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## 📖 Usage

### For Students

1. **Registration:**
   - Go to the registration page
   - Select "Student" role
   - Fill out the form

2. **Taking Quizzes:**
   - Browse available quizzes on "Browse Quizzes" page
   - Click "Take Quiz" to start
   - Answer the questions
   - View results and explanations after completion

3. **Tracking Progress:**
   - Dashboard - statistics and recent results
   - My History - complete history of solved quizzes
   - Leaderboard - rankings

### For Teachers

1. **Creating a Quiz:**
   - Go to "Create Quiz"
   - Fill in quiz information (title, description, category, difficulty)
   - Set parameters (time limit, number of attempts, passing threshold)
   - Save the quiz

2. **Adding Questions:**
   - Open the quiz and click "Manage Questions"
   - Add questions of various types
   - Specify correct answers
   - Add explanations (optional)

3. **Analytics:**
   - Go to "Reports" for the selected quiz
   - View attempt statistics
   - Analyze the most difficult questions

## 📁 Project Structure

```
techniki-internetowe/
├── accounts/              # User management application
│   ├── models.py         # User profile model
│   ├── views.py          # Registration, login, profile views
│   ├── forms.py          # User forms
│   └── urls.py           # Accounts app routing
├── quizzes/              # Main quiz application
│   ├── models.py         # Models: Quiz, Question, Answer, Result
│   ├── views.py          # Quiz, question, result views
│   ├── forms.py          # Quiz and question forms
│   ├── urls.py           # Quizzes app routing
│   └── management/       # Django commands
│       └── commands/
│           └── load_sample_data.py
├── quiz_platform/        # Project settings
│   ├── settings.py       # Django configuration
│   ├── urls.py           # Main routing
│   └── wsgi.py           # WSGI config
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── accounts/         # User account templates
│   └── quizzes/          # Quiz templates
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── main.js       # Application JavaScript
├── utils/                # Helper utilities
│   └── run_django.sh     # Server runner script
├── specification/        # Project documentation
├── manage.py             # Django CLI tool
├── pyproject.toml        # Project configuration and dependencies
└── README.md             # This file
```

## 👥 Test Accounts

After loading sample data, the following accounts are available:

### Teacher
- **Username:** teacher
- **Password:** teacher123
- **Permissions:** Create quizzes, manage questions, view reports

### Student
- **Username:** student
- **Password:** student123
- **Permissions:** Take quizzes, view results, leaderboards

## 🔧 Development

### Development Commands

**Run server:**
```bash
uv run python manage.py runserver
# or
./utils/run_django.sh
```

**Create migrations:**
```bash
uv run python manage.py makemigrations
```

**Apply migrations:**
```bash
uv run python manage.py migrate
```

**Create superuser:**
```bash
uv run python manage.py createsuperuser
```

**Collect static files (production):**
```bash
uv run python manage.py collectstatic
```

**Validate HTML:**
```bash
uv run python validate_html.py
```

**Run tests:**
```bash
uv run python manage.py test
```

### Database Structure

**Main models:**

- **User** - Django built-in model
- **Profile** - User extension (role, avatar, statistics)
- **Category** - Quiz categories
- **Quiz** - Quizzes with settings
- **Question** - Quiz questions
- **Answer** - Question answers
- **QuizAttempt** - Quiz attempt records
- **UserAnswer** - User responses

### Main URL Paths

- `/` - Homepage with featured quizzes
- `/quizzes/` - Browse all quizzes
- `/quiz/<id>/` - Quiz details
- `/quiz/<id>/take/` - Take quiz
- `/quiz/<id>/result/<attempt_id>/` - Results
- `/dashboard/` - User dashboard
- `/accounts/login/` - Login
- `/accounts/register/` - Registration
- `/accounts/profile/` - User profile
- `/admin/` - Django admin panel

### Security Features

- CSRF protection on all forms
- SQL injection prevention (Django ORM)
- XSS prevention (template auto-escaping)
- Password hashing (Django built-in)
- Session security
- Permission checks for teacher views

## 📝 Standards Compliance

- **HTML5:** All templates are HTML5 compliant
- **W3C Validation:** HTML code passes W3C validation
- **Responsiveness:** Works on mobile devices, tablets, and desktops
- **Accessibility:** Follows basic accessibility guidelines
- **Encoding:** All files use UTF-8
- **Browsers:** Tested in Firefox, Chrome, Edge

### HTML5 Validation

The project includes a script to check HTML5 compliance:

```bash
uv run python validate_html.py
```

The script:
- Renders Django templates
- Validates against W3C HTML5 standards
- Shows errors and warnings with line numbers
- Generates a summary report

## 🎨 Customization

### Adding New Categories

**Via admin panel:**
1. Go to `/admin/` → Categories → Add category

**Via Django shell:**
```python
from quizzes.models import Category
Category.objects.create(
    name="Mathematics",
    description="Math quizzes",
    color="#3498db",
    icon="fas fa-calculator"
)
```

### Creating Quizzes

1. Login as a teacher
2. Click "Create Quiz" in navigation
3. Fill in quiz details and settings
4. Add questions and answers
5. Publish when ready

## 🚀 Production Deployment

For production deployment:

1. **Django Configuration:**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for secrets

2. **Database:**
   - Switch to PostgreSQL or MySQL
   - Configure connection pooling

3. **Static Files:**
   - Run `collectstatic`
   - Configure CDN (optional)

4. **Web Server:**
   - Use Gunicorn as WSGI server
   - Configure Nginx as reverse proxy
   - Set up SSL certificate

5. **Security:**
   - Enable HTTPS
   - Configure security headers
   - Enable rate limiting

## ✅ Project Requirements Compliance

✅ **MPA Architecture:** Django templates with server-side rendering  
✅ **Database:** SQLite (development), can switch to PostgreSQL/MySQL  
✅ **Authorization:** Two-tier role system (Student/Teacher)  
✅ **Session Management:** Django session framework  
✅ **HTML5 Validation:** W3C compliant, includes validation script  
✅ **UTF-8 Encoding:** All files use UTF-8  
✅ **Responsive Design:** Works in Firefox, Chrome, Edge  
✅ **Client-side Enhancement:** JavaScript for timers, auto-save, validation  

## 🐛 Known Limitations

- SQLite as database (PostgreSQL recommended for production)
- No caching (Redis recommended for production)
- Images stored locally (CDN recommended for production)
- No CSV/PDF export for results (planned)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/feature-name`)
3. Commit your changes (`git commit -m 'Add: feature description'`)
4. Push to the branch (`git push origin feature/feature-name`)
5. Open a Pull Request

## 📄 License

Educational project for the *Techniki Internetowe* course.

## 📞 Contact

For questions about the project, contact the course instructor.

---

**Project:** Techniki Internetowe  
**Date:** January 2026  
**Version:** 1.0

