#!/bin/bash

# BLAAN Setup Script

echo "🚀 Starting BLAAN Trading Platform Setup..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Check MongoDB
echo "⚠️  Make sure MongoDB is running!"
echo "   Local: mongod"
echo "   Cloud: Use MongoDB Atlas connection string"
echo ""

# Setup Backend
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your credentials:"
    echo "   - NEWSAPI_KEY (get from https://newsapi.org)"
    echo "   - MONGODB_URI (if not using local)"
    echo "   - Email/Telegram/WhatsApp settings (optional)"
fi

cd ..

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Install dependencies
echo "Installing npm packages..."
npm install

# Create .env.local if needed
if [ ! -f ".env.local" ]; then
    echo "VITE_API_URL=http://localhost:5000" > .env.local
fi

cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Make sure MongoDB is running"
echo "3. Start the backend: cd backend && python main.py"
echo "4. In another terminal, start frontend: cd frontend && npm run dev"
echo "5. Open http://localhost:5173 in your browser"
echo ""
echo "🚀 Happy Trading!"
