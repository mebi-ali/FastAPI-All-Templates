import os
import subprocess

# ----------------------------
# 1. Project structure
# ----------------------------

structure = {
    "user_service": {
        "api": {
            "v1": {
                "user.py": "",
                "auth.py": ""
            },
            "deps.py": ""
        },
        "core": {
            "config.py": "",
            "security.py": "",
            "constants.py": ""
        },
        "db": {
            "base.py": "",
            "database.py": "",
            "utils.py": ""
        },
        "common": {
            "logging.py": "",
            "helpers.py": "",
            "exceptions": {
                "base.py": "",
                "http_exceptions.py": ""
            }
        },
        "user": {
            "models.py": "",
            "schemas.py": "",
            "service.py": "",
            "exceptions.py": "",
            "utils.py": ""
        },
        "auth": {
            "models.py": "",
            "schemas.py": "",
            "service.py": "",
            "exceptions.py": ""
        },
        "rbac": {
            "models.py": "",
            "schemas.py": "",
            "service.py": "",
            "permissions.py": ""
        },
        "tests": {
            "user": {},
            "auth": {},
            "conftest.py": ""
        },
        "main.py": """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Hello from scalable FastAPI project!"}
"""
    },
    "alembic": {}
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
            with open(os.path.join(path, '__init__.py'), 'w'): pass
        else:
            with open(path, 'w') as f:
                f.write(content)

# ----------------------------
# 2. Generate pyproject.toml
# ----------------------------

def write_pyproject():
    toml = """[project]
name = "xVision"
version = "0.1.0"
description = "A scalable FastAPI project"
dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "sqlalchemy[asyncio]",
    "asyncpg",
    "pydantic",
    "python-dotenv",
]

[build-system]
requires = ["uv"]
build-backend = "uv"
"""
    with open("pyproject.toml", "w") as f:
        f.write(toml)

# ----------------------------
# 3. Run uv installation
# ----------------------------

def install_dependencies():
    subprocess.run(["uv", "pip", "install", "--system", "-r", "pyproject.toml"])

# ----------------------------
# MAIN
# ----------------------------

if __name__ == "__main__":
    create_structure(".", structure)
    write_pyproject()
    print("📦 Project structure created.")
    print("📄 pyproject.toml created.")

    print("🚀 Installing dependencies with uv...")
    print("👉 You can run: uv venv && source .venv/bin/activate")
    print("👉 Then: uv pip install --system -r pyproject.toml")
