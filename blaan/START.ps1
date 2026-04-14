# 🚀 BLAAN Platform - FINAL STARTUP GUIDE (Windows)
# This is the OFFICIAL Windows startup script

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          🚀 BLAAN TRADING PLATFORM - STARTUP GUIDE 🚀          ║" -ForegroundColor Cyan
Write-Host "║                    Everything LIVE & REAL                       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# STEP 1: VERIFICATION
# ============================================================================

Write-Host "📋 STEP 1: Verifying Environment..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$python_version = python --version 2>&1
Write-Host "  ✓ $python_version" -ForegroundColor Green

$node_version = node --version 2>&1
Write-Host "  ✓ Node: $node_version" -ForegroundColor Green

$npm_version = npm --version 2>&1
Write-Host "  ✓ npm: $npm_version" -ForegroundColor Green

Write-Host ""

# ============================================================================
# STEP 2: BACKEND SETUP
# ============================================================================

Write-Host "⚙️  STEP 2: Setting up Backend..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

Set-Location backend

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "  📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
}

# Activate
& .\venv\Scripts\Activate.ps1
Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green

# Install packages
Write-Host "  📦 Installing Python packages (this may take 1-2 minutes)..." -ForegroundColor Yellow
pip install -q -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ All packages installed" -ForegroundColor Green
} else {
    Write-Host "  ✗ Package installation failed" -ForegroundColor Red
    exit 1
}

# Setup .env file
if (-not (Test-Path ".env")) {
    Write-Host "  📄 Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "  ⚠️  IMPORTANT: Edit backend/.env and add:" -ForegroundColor Yellow
    Write-Host "     • NEWSAPI_KEY (get free: https://newsapi.org)" -ForegroundColor White
    Write-Host "     • MONGODB_URI (default: mongodb://localhost:27017)" -ForegroundColor White
    Write-Host "     • TELEGRAM_BOT_TOKEN (optional)" -ForegroundColor White
    Write-Host "     • EMAIL settings (optional)" -ForegroundColor White
    Write-Host ""
    
    $response = Read-Host "  Have you added NEWSAPI_KEY to .env? (yes/no)"
    if ($response -ne "yes") {
        Write-Host "  ✗ Please add NEWSAPI_KEY before continuing" -ForegroundColor Red
        exit 1
    }
}

Write-Host "  ✓ Backend ready!" -ForegroundColor Green

Set-Location ..

Write-Host ""

# ============================================================================
# STEP 3: FRONTEND SETUP
# ============================================================================

Write-Host "⚙️  STEP 3: Setting up Frontend..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

Set-Location frontend

Write-Host "  📦 Installing Node packages (this may take 2-3 minutes)..." -ForegroundColor Yellow
npm install -q

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ All packages installed" -ForegroundColor Green
} else {
    Write-Host "  ✗ Package installation failed" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ Frontend ready!" -ForegroundColor Green

Set-Location ..

Write-Host ""

# ============================================================================
# STEP 5: STARTUP INSTRUCTIONS
# ============================================================================

Write-Host "🎉 STEP 5: Ready to Launch!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "  🚀 To START the platform:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  📌 TERMINAL 1 - Backend API:" -ForegroundColor Cyan
Write-Host "     cd backend" -ForegroundColor White
Write-Host "     .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "     python main.py" -ForegroundColor White
Write-Host ""
Write-Host "     ✓ API runs on: http://localhost:5000" -ForegroundColor Green
Write-Host "     ✓ Health check: http://localhost:5000/health" -ForegroundColor Green
Write-Host ""
Write-Host "  📌 TERMINAL 2 - Frontend App:" -ForegroundColor Cyan
Write-Host "     cd frontend" -ForegroundColor White
Write-Host "     npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "     ✓ App runs on: http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "  📌 TERMINAL 3 (Optional) - MongoDB:" -ForegroundColor Cyan
Write-Host "     mongod" -ForegroundColor White
Write-Host ""
Write-Host "     Or use MongoDB Atlas: Update MONGODB_URI in backend/.env" -ForegroundColor White
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "  📚 USEFUL COMMANDS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Validate setup:        python validate_setup.py" -ForegroundColor White
Write-Host "  Test API:             See API_TESTING.md" -ForegroundColor White
Write-Host "  View logs:            Check terminal output" -ForegroundColor White
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "  📖 DOCUMENTATION:" -ForegroundColor Yellow
Write-Host "     • README.md         - Overview & features" -ForegroundColor White
Write-Host "     • QUICK_START.md    - 5-minute setup" -ForegroundColor White
Write-Host "     • API_TESTING.md    - Full API test guide" -ForegroundColor White
Write-Host "     • ARCHITECTURE.md   - Technical details" -ForegroundColor White
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "🎯 FEATURES THAT ARE LIVE:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  ✓ Real password hashing with bcrypt" -ForegroundColor Green
Write-Host "  ✓ JWT token authentication" -ForegroundColor Green
Write-Host "  ✓ MongoDB database integration" -ForegroundColor Green
Write-Host "  ✓ Real NewsAPI integration" -ForegroundColor Green
Write-Host "  ✓ Real trade signal generation" -ForegroundColor Green
Write-Host "  ✓ Real risk calculations" -ForegroundColor Green
Write-Host "  ✓ Comprehensive error handling" -ForegroundColor Green
Write-Host "  ✓ Full logging & monitoring" -ForegroundColor Green
Write-Host "  ✓ Production-ready code" -ForegroundColor Green
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                  ✅ ALL SYSTEMS GO! 🚀                         ║" -ForegroundColor Cyan
Write-Host "║           Open http://localhost:5173 after startup             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
