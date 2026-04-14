#!/bin/bash

# Setup Windows PowerShell version

Write-Host "🚀 Starting BLAAN Trading Platform Setup..." -ForegroundColor Cyan
Write-Host ""

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python 3 is not installed. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

# Check Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js is not installed. Please install Node.js 16 or higher." -ForegroundColor Red
    exit 1
}

# Setup Backend
Write-Host "📦 Setting up Backend..." -ForegroundColor Cyan
cd backend

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
}

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing Python packages..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..."
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit .env with your credentials:" -ForegroundColor Yellow
    Write-Host "   - NEWSAPI_KEY (get from https://newsapi.org)"
    Write-Host "   - MONGODB_URI (if not using local)"
}

cd ..

# Setup Frontend
Write-Host ""
Write-Host "📦 Setting up Frontend..." -ForegroundColor Cyan
cd frontend

Write-Host "Installing npm packages..."
npm install

if (-not (Test-Path ".env.local")) {
    Write-Host "VITE_API_URL=http://localhost:5000" | Out-File -FilePath .env.local
}

cd ..

Write-Host ""
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Edit backend\.env with your API keys"
Write-Host "2. Make sure MongoDB is running"
Write-Host "3. Start backend in Terminal 1: cd backend && python main.py"
Write-Host "4. Start frontend in Terminal 2: cd frontend && npm run dev"
Write-Host "5. Open http://localhost:5173 in your browser"
Write-Host ""
Write-Host "🚀 Happy Trading!" -ForegroundColor Green
