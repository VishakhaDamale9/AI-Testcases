# Full-Stack Application

This repository contains a full-stack application with a FastAPI backend and React frontend.

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm 9 or higher
- PostgreSQL database

## Setup

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
PROJECT_NAME=MyFullStackApp
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=app
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin
```

### Quick Setup

Run the following command to set up both backend and frontend and run all tests:

```
setup_and_test.bat
```

Or you can set up each component separately:

### Backend Setup

```
setup_backend.bat
```

### Frontend Setup

```
setup_frontend.bat
```

## Running Tests

### Backend Tests

```
run_backend_tests.bat
```

### Frontend Tests

```
run_frontend_tests.bat
```

## Running the Application

### Backend

```
cd backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

### Frontend

```
cd frontend
npm run dev
```

## Project Structure

- `backend/`: FastAPI backend application
  - `app/`: Main application code
    - `api/`: API endpoints
    - `core/`: Core functionality
    - `tests/`: Test files
      - `features/`: BDD feature files
- `frontend/`: React frontend application
  - `src/`: Source code
  - `tests/`: Test files

## Dependencies

All dependencies are specified with exact versions in the requirements.txt files:

- `backend/requirements.txt`: Backend dependencies
- `frontend/requirements.txt`: Frontend dependencies