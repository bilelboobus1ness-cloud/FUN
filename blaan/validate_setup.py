#!/usr/bin/env python3
"""
BLAAN Setup Validation Script
Verifies that everything is installed correctly and LIVE
"""

import os
import sys
import subprocess
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"{Colors.GREEN}✓ Python {version.major}.{version.minor}{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}✗ Python 3.9+ required (found {version.major}.{version.minor}){Colors.END}")
        return False

def check_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"{Colors.GREEN}✓ {package_name}{Colors.END}")
        return True
    except ImportError:
        print(f"{Colors.RED}✗ {package_name} (run: pip install {package_name}){Colors.END}")
        return False

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"{Colors.GREEN}✓ {description}{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}✗ {description} (not found){Colors.END}")
        return False

def check_mongodb():
    """Check MongoDB connection"""
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000)
        client.admin.command('ismaster')
        print(f"{Colors.GREEN}✓ MongoDB (local){Colors.END}")
        return True
    except:
        print(f"{Colors.YELLOW}⚠ MongoDB (not running locally - use MongoDB Atlas){Colors.END}")
        return False

def check_env_file():
    """Check .env file"""
    env_path = 'backend/.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            content = f.read()
            if 'NEWSAPI_KEY=' in content and not content.strip().endswith('demo_key'):
                print(f"{Colors.GREEN}✓ .env file (configured){Colors.END}")
                return True
            else:
                print(f"{Colors.YELLOW}⚠ .env file (missing API keys){Colors.END}")
                return False
    else:
        print(f"{Colors.RED}✗ .env file not found{Colors.END}")
        return False

def validate_setup():
    """Run all validation checks"""
    
    print_header("BLAAN Setup Validation")
    
    all_good = True
    
    # Python version
    print(f"{Colors.BLUE}[1] Python Environment{Colors.END}")
    if not check_python():
        all_good = False
    
    # Python packages
    print(f"\n{Colors.BLUE}[2] Required Python Packages{Colors.END}")
    packages = [
        ('Flask', 'flask'),
        ('Flask-CORS', 'flask_cors'),
        ('Flask-JWT-Extended', 'flask_jwt_extended'),
        ('PyMongo', 'pymongo'),
        ('python-dotenv', 'dotenv'),
        ('newsapi', 'newsapi'),
        ('Requests', 'requests'),
        ('bcrypt', 'bcrypt'),
        ('email-validator', 'email_validator'),
    ]
    
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            all_good = False
    
    # Project files
    print(f"\n{Colors.BLUE}[3] Project Files{Colors.END}")
    files = [
        ('backend/requirements.txt', 'Backend dependencies'),
        ('backend/.env.example', 'Environment template'),
        ('backend/main.py', 'Flask app'),
        ('frontend/package.json', 'Frontend dependencies'),
        ('frontend/index.html', 'Frontend entry'),
    ]
    
    for filepath, description in files:
        if not check_file(filepath, description):
            all_good = False
    
    # Database
    print(f"\n{Colors.BLUE}[4] Database{Colors.END}")
    check_mongodb()
    
    # Environment configuration
    print(f"\n{Colors.BLUE}[5] Configuration{Colors.END}")
    if not check_env_file():
        all_good = False
    
    # Summary
    print_header("Summary")
    
    if all_good:
        print(f"{Colors.GREEN}✓ All checks passed! BLAAN is ready to run!{Colors.END}\n")
        print("Next steps:")
        print("  1. Start backend:  cd backend && python main.py")
        print("  2. Start frontend: cd frontend && npm run dev")
        print("  3. Open: http://localhost:5173")
        print()
    else:
        print(f"{Colors.RED}✗ Some checks failed. Fix issues above before running.{Colors.END}\n")
        print("Common fixes:")
        print("  - Install packages: pip install -r backend/requirements.txt")
        print("  - Copy .env: cp backend/.env.example backend/.env")
        print("  - Edit .env: Add your NEWSAPI_KEY")
        print("  - Start MongoDB: mongod (or use MongoDB Atlas)")
        print()
    
    return all_good

if __name__ == '__main__':
    success = validate_setup()
    sys.exit(0 if success else 1)
