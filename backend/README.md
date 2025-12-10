# Backend Documentation

FastAPI backend with SQLModel ORM, PostgreSQL database, JWT authentication, and comprehensive testing.

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- Virtual environment tool (venv)

### Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup

```bash
# Run migrations
alembic upgrade head

# Create a new migration (after model changes)
alembic revision --autogenerate -m "Description of changes"
```

### Running the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_users.py

# Run with verbose output
pytest -v
```

### BDD Tests with Behave

```bash
# Run all BDD tests
python -m behave app/tests/features

# Run specific feature
python -m behave app/tests/features/users.feature

# Run with specific tags
python -m behave --tags=@authentication
```

## 🔍 Code Quality

### Linting

```bash
# Check code with ruff
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

### Type Checking

```bash
# Run mypy type checker
mypy .
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/                 # API route handlers
│   │   ├── users.py
│   │   ├── auth.py
│   │   └── ...
│   ├── core/                # Core configuration
│   │   ├── config.py        # Settings and configuration
│   │   ├── security.py      # Security utilities
│   │   └── ...
│   ├── tests/               # Test files
│   │   ├── features/        # BDD feature files
│   │   └── ...
│   ├── models.py            # SQLModel database models
│   ├── crud.py              # Database CRUD operations
│   ├── schemas.py           # Pydantic schemas
│   ├── deps.py              # Dependencies
│   └── main.py              # FastAPI application
├── alembic/                 # Database migrations
│   ├── versions/            # Migration files
│   └── env.py
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Project configuration
└── alembic.ini              # Alembic configuration
```

## 🔧 Configuration

Configuration is managed through environment variables and `app/core/config.py`.

### Key Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `FIRST_SUPERUSER_EMAIL`: Initial admin email
- `FIRST_SUPERUSER_PASSWORD`: Initial admin password

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS middleware configured
- SQL injection protection via SQLModel
- Input validation with Pydantic

## 🛠️ Development

### Adding a New Endpoint

1. Create route handler in `app/api/`
2. Define Pydantic schemas if needed
3. Add CRUD operations in `app/crud.py`
4. Update models in `app/models.py` if needed
5. Write tests
6. Generate BDD tests using the test generator

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## 📊 Coverage Reports

After running tests with coverage:

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# View report
# Open htmlcov/index.html in browser
```

## 🐛 Debugging

### Enable Debug Logging

Set `DEBUG=True` in your environment or configuration.

### Interactive Debugging

Use Python debugger:
```python
import pdb; pdb.set_trace()
```

Or use breakpoint():
```python
breakpoint()
```

## 📦 Dependencies

Main dependencies:
- **FastAPI**: Modern web framework
- **SQLModel**: SQL databases with Python objects
- **Alembic**: Database migrations
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server
- **Pytest**: Testing framework
- **Behave**: BDD testing

See `requirements.txt` for complete list.
