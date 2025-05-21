A secure user management system with Role-Based Access Control (RBAC) built with FastAPI, FastORM, and PostgreSQL.

## Features
- ✅ **JWT Authentication** (OAuth2 + Bearer tokens)
- 🔐 **Role-Based Access Control** (RBAC)
- 👥 User management (Create/Read/Update/Delete)
- 🛡️ Permission granularity
- 🚀 Async database operations with FastORM

---

## 🛠 Setup Guide

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Pipenv (recommended) or `venv`

### Step 1: Clone the Repository
```bash
cd Desktop
git clone https://github.com/your-repo/user-management-fastapi.git
```

### Step 2: Clone the Repository
```bash
python3 -m venv .venv
source .venv/bin/activate
```


### Step 3: Create .env file and paste these in your env
```bash
# Environment
ENVIRONMENT=development
DEBUG_MODE=True

# Application
PROJECT_NAME=User Service
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/user-service

# JWT / Authentication
JWT_SECRET_KEY=super-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 4: Install Dependencies
```bash
pip install -r user_service/requirements.txt
```

### Step 5: Start the Application
```bah
uvicorn user_service.main:app --reload
```

