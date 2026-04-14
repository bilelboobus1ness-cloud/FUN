# BLAAN Quick Start Guide

## 5-Minute Setup

### Step 1: Prerequisites
Ensure you have:
- ✅ Python 3.9+
- ✅ Node.js 16+
- ✅ MongoDB (local or MongoDB Atlas)
- ✅ NewsAPI key (free at https://newsapi.org)

### Step 2: Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Edit .env with your credentials (especially NEWSAPI_KEY)
python main.py
```

Backend runs on: `http://localhost:5000`

### Step 3: Frontend Setup (in new terminal)
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: `http://localhost:5173`

### Step 4: Database Setup
Make sure MongoDB is running:
```bash
# Local MongoDB
mongod

# Or use MongoDB Atlas cloud database
# Update MONGODB_URI in .env
```

## Usage Flow

1. **Register/Login** - Create your account
2. **Setup Account** - Add broker details and account balance
3. **Check News** - Browse market news by currency pair
4. **Generate Signal** - Create trade signals from news
5. **Calculate Risk** - Use risk calculator for lot sizing
6. **Get Notifications** - Enable Email/WhatsApp/Telegram
7. **Execute Trade** - Execute signals in your broker

## API Testing with cURL

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "trader@example.com",
    "password": "password123",
    "full_name": "John Trader"
  }'
```

### Create Account
```bash
curl -X POST http://localhost:5000/api/account/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-id-here",
    "broker_name": "Forex.com",
    "account_number": "12345",
    "balance": 10000,
    "risk_percentage": 2
  }'
```

### Get Forex News
```bash
curl http://localhost:5000/api/news/categorized
```

### Calculate Lot Size
```bash
curl -X POST http://localhost:5000/api/trades/calculate-lot-size \
  -H "Content-Type: application/json" \
  -d '{
    "account_balance": 10000,
    "risk_percentage": 2,
    "entry_price": 1.0850,
    "stop_loss": 1.0800,
    "take_profit": 1.0950
  }'
```

## Environment Variables

### Required
- **MONGODB_URI**: MongoDB connection string
- **NEWSAPI_KEY**: Get from https://newsapi.org

### Optional (for notifications)
- **TELEGRAM_BOT_TOKEN**: Telegram bot token
- **TELEGRAM_CHAT_ID**: Your Telegram chat ID
- **WHATSAPP_ACCOUNT_SID**: Twilio account SID
- **WHATSAPP_AUTH_TOKEN**: Twilio auth token
- **EMAIL_SENDER**: Your email for sending alerts
- **EMAIL_PASSWORD**: Email app password

## Troubleshooting

### Port Already in Use
```bash
# Change port in backend main.py (port=5001)
# Or kill the process using the port
lsof -i :5000  # Find process
kill -9 <PID>   # Kill process
```

### MongoDB Connection Error
```bash
# Make sure MongoDB is running
mongod

# Or check your MongoDB Atlas connection string
# Update MONGODB_URI in .env
```

### API Key Errors
```bash
# Ensure .env file exists with all required keys
# NewsAPI keys are free at https://newsapi.org
# Check you're using the correct API key format
```

### CORS Errors
```bash
# Backend Flask already has CORS enabled
# If still getting errors, check:
# - Backend is running on http://localhost:5000
# - Frontend is on http://localhost:5173
```

## Performance Tips

- Keep MongoDB index on popular fields
- Cache news data to avoid repeated API calls
- Implement pagination for large signal lists
- Use WebSockets for real-time updates (future improvement)

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Use environment variables for all secrets
- [ ] Validate all user inputs
- [ ] Implement proper authentication (JWT token)
- [ ] Use HTTPS in production
- [ ] Secure MongoDB with password
- [ ] Don't commit .env files to git

## Next Steps

1. **Customize UI** - Modify colors in Navbar.css and Dashboard.css
2. **Add More Signals** - Integrate with more news sources
3. **Broker Integration** - Add broker API connections
4. **Advanced Analytics** - Add performance metrics and statistics
5. **Mobile App** - Build mobile version with React Native

## Support Resources

- Flask Documentation: https://flask.palletsprojects.com
- React Documentation: https://react.dev
- MongoDB Documentation: https://docs.mongodb.com
- NewsAPI Documentation: https://newsapi.org/docs
- Telegram Bot API: https://core.telegram.org/bots/api

---

Happy Trading! 🚀📈
