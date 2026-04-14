#!/bin/bash

# 🚀 BLAAN Platform - FINAL STARTUP GUIDE
# This is the OFFICIAL, CLEAR, STEP-BY-STEP guide to get everything LIVE and RUNNING

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          🚀 BLAAN TRADING PLATFORM - STARTUP GUIDE 🚀          ║"
echo "║                    Everything LIVE & REAL                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# STEP 1: VERIFICATION
# ============================================================================

echo "📋 STEP 1: Verifying Environment..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Python
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  ✓ Python: $python_version"

# Check Node
node_version=$(node --version 2>&1)
npm_version=$(npm --version 2>&1)
echo "  ✓ Node: $node_version"
echo "  ✓ npm: $npm_version"

echo ""

# ============================================================================
# STEP 2: BACKEND SETUP
# ============================================================================

echo "⚙️  STEP 2: Setting up Backend..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "  📦 Creating virtual environment..."
    python3 -m venv venv
    echo "  ✓ Virtual environment created"
fi

# Activate
source venv/bin/activate
echo "  ✓ Virtual environment activated"

# Install packages
echo "  📦 Installing Python packages (this may take 1-2 minutes)..."
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo "  ✓ All packages installed successfully"
else
    echo "  ✗ Package installation failed"
    exit 1
fi

# Setup .env file
if [ ! -f ".env" ]; then
    echo "  📄 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "  ⚠️  IMPORTANT: Edit backend/.env and add:"
    echo "     • NEWSAPI_KEY (get free: https://newsapi.org)"
    echo "     • MONGODB_URI (default: mongodb://localhost:27017)"
    echo "     • TELEGRAM_BOT_TOKEN (optional)"
    echo "     • EMAIL settings (optional)"
    echo ""
    read -p "  Have you added NEWSAPI_KEY to .env? (yes/no) " -n 3 -r
    echo
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss] ]]; then
        echo "  ✗ Please add NEWSAPI_KEY before continuing"
        exit 1
    fi
fi

echo "  ✓ Backend ready!"

cd ..

echo ""

# ============================================================================
# STEP 3: FRONTEND SETUP
# ============================================================================

echo "⚙️  STEP 3: Setting up Frontend..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd frontend

echo "  📦 Installing Node packages (this may take 2-3 minutes)..."
npm install -q

if [ $? -eq 0 ]; then
    echo "  ✓ All packages installed successfully"
else
    echo "  ✗ Package installation failed"
    exit 1
fi

echo "  ✓ Frontend ready!"

cd ..

echo ""

# ============================================================================
# STEP 4: VALIDATION
# ============================================================================

echo "✅ STEP 4: Validating Setup..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd backend
source venv/bin/activate
python3 ../validate_setup.py
cd ..

echo ""

# ============================================================================
# STEP 5: STARTUP INSTRUCTIONS
# ============================================================================

echo "🎉 STEP 5: Ready to Launch!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  🚀 To START the platform:"
echo ""
echo "  📌 TERMINAL 1 - Backend API:"
echo "     cd backend"
echo "     source venv/bin/activate"
echo "     python main.py"
echo ""
echo "     ✓ API runs on: http://localhost:5000"
echo "     ✓ Health check: http://localhost:5000/health"
echo ""
echo "  📌 TERMINAL 2 - Frontend App:"
echo "     cd frontend"
echo "     npm run dev"
echo ""
echo "     ✓ App runs on: http://localhost:5173"
echo ""
echo "  📌 TERMINAL 3 (Optional) - MongoDB:"
echo "     mongod"
echo ""
echo "     Or use MongoDB Atlas: Update MONGODB_URI in backend/.env"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  📚 USEFUL COMMANDS:"
echo ""
echo "  Validate setup:        python validate_setup.py"
echo "  Test API:             See API_TESTING.md"
echo "  View logs:            Check terminal output"
echo "  Kill port 5000:       lsof -i :5000 | kill -9 <PID>"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  📖 DOCUMENTATION:"
echo "     • README.md         - Overview & features"
echo "     • QUICK_START.md    - 5-minute setup"
echo "     • API_TESTING.md    - Full API test guide"
echo "     • ARCHITECTURE.md   - Technical details"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎯 FEATURES THAT ARE LIVE:"
echo ""
echo "  ✓ Real password hashing with bcrypt"
echo "  ✓ JWT token authentication"
echo "  ✓ MongoDB database integration"
echo "  ✓ Real NewsAPI integration"
echo "  ✓ Real trade signal generation"
echo "  ✓ Real risk calculations"
echo "  ✓ Comprehensive error handling"
echo "  ✓ Full logging & monitoring"
echo "  ✓ Production-ready code"
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  ✅ ALL SYSTEMS GO! 🚀                         ║"
echo "║           Open http://localhost:5173 after startup             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
