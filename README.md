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
git clone git@github.com:mebi-ali/FastAPI-All-Templates.git
```

### Step 2: Change the branch for FastORM
```bash
git checkout features/FastORM-user-service
```

### Step 3: Clone the Repository
```bash
python3 -m venv .venv
source .venv/bin/activate
```


### Step 4: Create .env file and paste these in your env 
**replace username, password and dbname with your actual values**
```bash
# Environment
ENVIRONMENT=development
DEBUG_MODE=True

# Application
PROJECT_NAME=User Service
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# JWT / Authentication
JWT_SECRET_KEY=super-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 5: Install Dependencies
```bash
pip install -r user_service/requirements.txt
```

### Step 6: Start the Application
```bah
uvicorn user_service.main:app --reload
```

