# Fullstack Application with Automated BDD Test Generation

A modern fullstack application featuring a **FastAPI** backend with **SQLModel** ORM and a **React** frontend with **Chakra UI**, along with AI-powered BDD test generation using Groq API.

## 🚀 Features

- **Backend**: FastAPI with SQLModel, PostgreSQL, JWT authentication, and Alembic migrations
- **Frontend**: React with TypeScript, Chakra UI, TanStack Router, and TanStack Query
- **AI-Powered Testing**: Automated BDD test generation using Groq API
- **Coverage Analysis**: Intelligent test gap detection and coverage reporting
- **Type Safety**: Full TypeScript support with auto-generated API client

## 📋 Prerequisites

- **Python** 3.10 or higher
- **Node.js** 18 or higher
- **PostgreSQL** database
- **Groq API Key** (for BDD test generation)

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/VishakhaDamale9/AI-Testcases.git
cd AI-Testcases
```

### 2. Environment Configuration

Create `.env` files in both root and frontend directories:

**Root `.env`** (for BDD test generation):
```bash
GROQ_API_KEY=your_groq_api_key_here
```

**Frontend `.env`** (see `frontend/.env.example`):
```bash
VITE_API_URL=http://localhost:8000
```

**Backend configuration** is managed through environment variables or `backend/app/core/config.py`.

### 3. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🧪 BDD Test Generation

This project includes AI-powered BDD test generation using the Groq API.

### Generate BDD Tests

```bash
# From the project root
python bdd_test_generator.py

# Generate tests for a specific endpoint
python bdd_test_generator.py --endpoint backend/app/api/users.py

# Use a different Groq model
python bdd_test_generator.py --model llama-3.1-70b-versatile
```

### Run BDD Tests

```bash
cd backend
python -m behave app/tests/features
```

### Analyze Coverage Gaps

```bash
# Generate coverage report first
cd backend
pytest --cov=app --cov-report=xml

# Analyze coverage gaps
cd ..
python analyze_coverage_gaps.py
```

## 📁 Project Structure

```
AI-Testcases/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API route handlers
│   │   ├── core/              # Core configuration
│   │   ├── models.py          # SQLModel database models
│   │   ├── crud.py            # Database operations
│   │   ├── main.py            # FastAPI application entry
│   │   └── tests/             # Test files
│   │       └── features/      # BDD feature files
│   ├── alembic/               # Database migrations
│   ├── requirements.txt       # Python dependencies
│   └── pyproject.toml         # Project configuration
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── routes/            # Route components
│   │   └── client/            # Auto-generated API client
│   ├── package.json           # Node dependencies
│   └── vite.config.ts         # Vite configuration
├── bdd_test_generator.py      # AI-powered BDD test generator
├── analyze_coverage_gaps.py   # Coverage analysis tool
├── prompt_templates.json      # Groq API prompt templates
└── README.md                  # This file
```

## 🔧 Available Scripts

### Backend

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run linting
ruff check .

# Run type checking
mypy .

# Format code
ruff format .
```

### Frontend

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint and format
npm run lint

# Generate API client
npm run generate-client
```

## 🔐 Security Notes

- Never commit `.env` files to version control
- Keep your `GROQ_API_KEY` and database credentials secure
- Use environment variables for all sensitive configuration
- Review the `.gitignore` file to ensure sensitive files are excluded

## 📚 Additional Documentation

- [Backend Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## 📄 About

This project demonstrates automated BDD test generation using AI, combining modern fullstack development practices with intelligent test coverage analysis.
