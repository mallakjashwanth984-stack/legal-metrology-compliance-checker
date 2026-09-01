# Development Setup Guide

## Prerequisites Installation

### Python (Backend)
```bash
# Check Python version (3.8+)
python3 --version

# Install Python
# macOS: brew install python3
# Ubuntu: sudo apt-get install python3 python3-pip python3-venv
# Windows: Download from python.org
```

### Node.js (Frontend)
```bash
# Check Node version (16+)
node --version
npm --version

# Install Node
# macOS: brew install node
# Ubuntu: sudo apt-get install nodejs npm
# Windows: Download from nodejs.org
```

### PostgreSQL
```bash
# Install PostgreSQL (12+)
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql postgresql-contrib
# Windows: Download installer from postgresql.org

# Start PostgreSQL
# macOS: brew services start postgresql
# Ubuntu: sudo service postgresql start
# Windows: Use Services manager or pgAdmin

# Create database
sudo -u postgres createdb metrology_db
sudo -u postgres createuser metrology_user
```

### Tesseract OCR
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# macOS
brew install tesseract

# Windows
# Download: https://github.com/UB-Mannheim/tesseract/wiki
```

## IDE/Editor Setup

### VS Code (Recommended)

**Extensions**
- Python (ms-python.python)
- Flask (donjayamanne.flask)
- ES7+ React/Redux/React-Native snippets
- TypeScript Vue Plugin
- Prettier - Code formatter
- ESLint
- Thunder Client / REST Client

**Settings** (.vscode/settings.json)
```json
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
  },
  "[typescript]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### PyCharm (Alternative for Backend)
- Configure Python interpreter
- Set project SDK
- Enable Flask support
- Configure database connections

### WebStorm (Alternative for Frontend)
- Configure Node interpreter
- Enable TypeScript support
- Configure ESLint and Prettier

## Local Development Workflow

### Step 1: Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Edit .env with your settings
# Key variables:
# DATABASE_URL=postgresql://metrology_user:password@localhost:5432/metrology_db
# JWT_SECRET_KEY=your_secret_key_change_in_production
# TESSERCE_CMD=/usr/bin/tesseract (or path on your system)

# Initialize database
flask db upgrade

# Create initial admin user (optional)
python -c "from app import create_app, db; from models.user import User; app = create_app(); app.app_context().push(); u = User(username='admin', email='admin@example.com', role='admin'); u.set_password('admin123'); db.session.add(u); db.session.commit(); print('Admin user created')"

# Run development server
python app.py
# Server will be at http://localhost:5000
```

### Step 2: Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env.local
# Edit .env.local with:
# NEXT_PUBLIC_API_URL=http://localhost:5000/api

# Run development server
npm run dev
# Frontend will be at http://localhost:3000
```

### Step 3: Test the Application

```bash
# In browser, navigate to http://localhost:3000
# 1. Create new account at /register
# 2. Login at /login
# 3. Go to /upload to test product upload
# 4. View /dashboard for analytics
```

## Testing

### Backend Tests

```bash
cd backend

# Install pytest
pip install pytest pytest-cov

# Create tests directory
mkdir tests

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

### Frontend Tests

```bash
cd frontend

# Install testing dependencies
npm install --save-dev jest @testing-library/react @testing-library/jest-dom

# Run tests
npm test

# With coverage
npm test -- --coverage
```

## Database Management

### Create Migrations

```bash
cd backend

# Generate migration from model changes
flask db migrate -m "Description of changes"

# Review generated migration file in migrations/versions/

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

### Connect to Database

```bash
# PostgreSQL CLI
psql -U metrology_user -d metrology_db

# List tables
\dt

# Describe table
\d table_name

# Exit
\q
```

## Debugging

### Backend Debugging

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# In VS Code, add to .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "development"
      },
      "args": ["run"],
      "jinja": true,
      "justMyCode": true
    }
  ]
}
```

### Frontend Debugging

```bash
# React DevTools browser extension
# Chrome: https://chrome.google.com/webstore
# Firefox: https://addons.mozilla.org

# VS Code React extension
npm install -g vscode-react-native
```

## Environment Variables Reference

### Backend (.env)
```bash
# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py
FLASK_DEBUG=1

# Database
DATABASE_URL=postgresql://metrology_user:password@localhost:5432/metrology_db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# JWT
JWT_SECRET_KEY=your_very_secret_key_change_in_production
JWT_ACCESS_TOKEN_EXPIRES=3600

# File Upload
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=52428800  # 50MB in bytes

# OCR
TESSERACT_CMD=/usr/bin/tesseract  # Adjust path for your OS

# CORS
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000/api
NEXT_PUBLIC_APP_NAME=Legal Metrology Compliance Checker
```

## Common Issues

### Issue: ModuleNotFoundError
```
Solution:
1. Ensure virtual environment is activated
2. Run: pip install -r requirements.txt
3. Check Python version compatibility
```

### Issue: Tesseract not found
```
Solution:
1. Install Tesseract on your system
2. Update TESSERACT_CMD in .env with correct path
3. Restart Flask server
```

### Issue: PostgreSQL connection refused
```
Solution:
1. Ensure PostgreSQL service is running
2. Check DATABASE_URL in .env
3. Verify database exists: psql -l
4. Verify user and password are correct
```

### Issue: Port already in use
```
Solution:
# Find and kill process using port
lsof -i :5000  # Check what's using port 5000
kill -9 <PID>  # Kill the process

# Or use different port
python app.py --port 5001
```

## Performance Tips

1. **Database Indexing**: Add indexes to frequently queried columns
2. **Query Optimization**: Use pagination and limit results
3. **Image Optimization**: Compress images before storage
4. **Caching**: Implement Redis for session/data caching
5. **Frontend Optimization**: Use Code splitting and lazy loading

## Code Style

### Python (Backend)
```bash
# Format with black
pip install black
black .

# Lint with pylint
pip install pylint
pylint backend/

# Type checking with mypy
pip install mypy
mypy .
```

### TypeScript/JavaScript (Frontend)
```bash
# Format with Prettier
npm run format

# Lint with ESLint
npm run lint

# Fix issues
npm run lint -- --fix
```

## Useful Commands

```bash
# Backend
flask shell              # Interactive Python shell
flask db current        # Show current database version
flask db heads          # Show available migrations

# Frontend
npm run build           # Build for production
npm run start           # Start production server
npm run analyze         # Analyze bundle size
```

## Further Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Tesseract OCR Documentation](https://github.com/tesseract-ocr/tesseract)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
