# 🧪 BLAAN API Testing Guide

Complete guide to test every endpoint and verify everything is LIVE and WORKING.

---

## ✅ Pre-Test Checklist

Before running tests:
- [ ] Backend running: `python main.py`
- [ ] MongoDB running (local or Atlas)
- [ ] `.env` file configured with `NEWSAPI_KEY`
- [ ] Python 3.9+
- [ ] All dependencies installed

---

## 🚀 Quick Test Commands

### Health Check (No Auth Required)
```bash
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "BLAAN Trading API",
  "database": "✓ Connected",
  "version": "1.0.0"
}
```

---

## 📝 User Registration & Authentication

### 1. Register New User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "trader@example.com",
    "password": "SecurePass123",
    "full_name": "John Trader"
  }'
```

**Expected Response (201 Created):**
```json
{
  "message": "✓ Registration successful",
  "user_id": "abc123...",
  "email": "trader@example.com"
}
```

**Test Cases:**
```bash
# ✗ Missing fields
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com"}'
# Response: 400 - Missing required fields

# ✗ Weak password (< 8 characters)
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@test.com",
    "password": "short",
    "full_name": "Test User"
  }'
# Response: 400 - Password must be 8+ characters

# ✗ Invalid email
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "not-an-email",
    "password": "ValidPass123",
    "full_name": "Test User"
  }'
# Response: 400 - Invalid email format
```

---

### 2. User Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "trader@example.com",
    "password": "SecurePass123"
  }'
```

**Expected Response (200 OK):**
```json
{
  "message": "✓ Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "abc123...",
  "email": "trader@example.com",
  "full_name": "John Trader"
}
```

**Test Cases:**
```bash
# ✗ Wrong password
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "trader@example.com",
    "password": "WrongPassword"
  }'
# Response: 401 - Invalid email or password

# ✗ Non-existent user
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nonexistent@example.com",
    "password": "SomePassword123"
  }'
# Response: 401 - Invalid email or password
```

---

### 3. Get Current User (Requires Auth)
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**Expected Response:**
```json
{
  "user_id": "abc123...",
  "email": "trader@example.com",
  "full_name": "John Trader",
  "notification_preferences": {
    "email": true,
    "whatsapp": false,
    "telegram": false
  }
}
```

---

## 🏦 Trading Account Management

### 1. Create Trading Account
```bash
# First, get user_id from login response
USER_ID="your_user_id_here"

curl -X POST http://localhost:5000/api/account/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "'$USER_ID'",
    "broker_name": "Forex.com",
    "account_number": "12345678",
    "api_key": "your_api_key_optional",
    "balance": 10000,
    "currency": "USD",
    "leverage": 100,
    "risk_percentage": 2
  }'
```

**Expected Response (201 Created):**
```json
{
  "message": "Account created successfully",
  "account_id": "def456..."
}
```

---

### 2. Get User's Accounts
```bash
USER_ID="abc123..."

curl http://localhost:5000/api/account/$USER_ID
```

**Expected Response:**
```json
{
  "accounts": [
    {
      "_id": "def456...",
      "user_id": "abc123...",
      "broker_name": "Forex.com",
      "account_number": "12345678",
      "current_balance": 10000,
      "currency": "USD",
      "leverage": 100,
      "risk_percentage": 2,
      "status": "active"
    }
  ]
}
```

---

### 3. Get Risk Info for Account
```bash
ACCOUNT_ID="def456..."

curl http://localhost:5000/api/account/$ACCOUNT_ID/risk-info
```

**Expected Response:**
```json
{
  "account_id": "def456...",
  "balance": 10000,
  "risk_percentage": 2,
  "risk_amount": 200,
  "recommended_lot_size": 0.4,
  "currency": "USD",
  "leverage": 100
}
```

---

### 4. Update Account Balance
```bash
ACCOUNT_ID="def456..."

curl -X PUT http://localhost:5000/api/account/$ACCOUNT_ID/update-balance \
  -H "Content-Type: application/json" \
  -d '{
    "new_balance": 10500
  }'
```

**Expected Response:**
```json
{
  "message": "Balance updated successfully"
}
```

---

## 📰 Market News

### 1. Get Categorized News by Currency Pair
```bash
curl http://localhost:5000/api/news/categorized
```

**Expected Response:**
```json
{
  "categorized_news": {
    "EUR": [
      {
        "source": {"name": "Reuters"},
        "title": "ECB announces new monetary policy...",
        "description": "...",
        "url": "...",
        "publishedAt": "2024-04-14T10:30:00Z",
        "image": "..."
      }
    ],
    "USD": [...],
    "GBP": [...]
  },
  "total_articles": 45
}
```

---

### 2. Get High-Impact News Only
```bash
curl http://localhost:5000/api/news/high-impact
```

**Expected Response:**
```json
{
  "high_impact_articles": [
    {
      "title": "FED raises interest rates unexpectedly",
      "description": "...",
      "source": {"name": "Bloomberg"},
      "publishedAt": "2024-04-14T14:00:00Z"
    }
  ],
  "count": 8
}
```

---

### 3. Get News for Specific Currency
```bash
curl http://localhost:5000/api/news/currency/EUR
```

---

## 📊 Trade Signals

### 1. Create Trade Signal
```bash
curl -X POST http://localhost:5000/api/trades/create \
  -H "Content-Type: application/json" \
  -d '{
    "currency_pair": "EURUSD",
    "entry_price": 1.0850,
    "stop_loss": 1.0800,
    "take_profit": 1.0950,
    "execution_time": "2024-04-14T10:30:00Z",
    "signal_type": "BUY",
    "news_source": "Reuters",
    "lot_size": 0.4,
    "risk_amount": 200
  }'
```

**Expected Response:**
```json
{
  "message": "Trade signal created successfully",
  "signal_id": "sig789..."
}
```

---

### 2. Get All Signals
```bash
curl http://localhost:5000/api/trades/all
```

**Expected Response:**
```json
{
  "signals": [
    {
      "_id": "sig789...",
      "currency_pair": "EURUSD",
      "entry_price": 1.0850,
      "stop_loss": 1.0800,
      "take_profit": 1.0950,
      "signal_type": "BUY",
      "lot_size": 0.4,
      "risk_amount": 200,
      "status": "pending",
      "created_at": "2024-04-14T10:30:00Z"
    }
  ]
}
```

---

### 3. Get Signals for Specific Pair
```bash
curl http://localhost:5000/api/trades/pair/EURUSD
```

---

### 4. Get Pending Signals Only
```bash
curl http://localhost:5000/api/trades/pending
```

---

### 5. Calculate Lot Size
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

**Expected Response:**
```json
{
  "lot_size": 0.4,
  "potential_loss": 200,
  "potential_profit": 400,
  "reward_risk_ratio": 2.0
}
```

---

### 6. Update Signal Status
```bash
SIGNAL_ID="sig789..."

curl -X PUT http://localhost:5000/api/trades/$SIGNAL_ID/update-status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "executed"
  }'
```

---

## 🧪 Testing with Python

### Complete Test Script
```python
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_registration():
    """Test user registration"""
    response = requests.post(
        f'{BASE_URL}/api/auth/register',
        json={
            'email': 'test_trader@example.com',
            'password': 'TestPass12345',
            'full_name': 'Test Trader'
        }
    )
    print(f"Registration: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json().get('user_id')

def test_login():
    """Test user login"""
    response = requests.post(
        f'{BASE_URL}/api/auth/login',
        json={
            'email': 'test_trader@example.com',
            'password': 'TestPass12345'
        }
    )
    print(f"\nLogin: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json().get('access_token')

def test_health():
    """Check server health"""
    response = requests.get(f'{BASE_URL}/health')
    print(f"\nHealth Check: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

if __name__ == '__main__':
    print("🧪 Starting BLAAN API Tests...\n")
    
    test_health()
    user_id = test_registration()
    token = test_login()
    
    print(f"\n✓ All tests completed!")
    print(f"Save token for authenticated requests: {token[:20]}...")
```

---

## ✅ Test Checklist

- [ ] Health check returns 200 with database status
- [ ] User registration validates email format
- [ ] User registration rejects weak passwords
- [ ] Login returns JWT token
- [ ] JWT token works for authenticated endpoints
- [ ] Account creation stores broker info correctly
- [ ] Risk calculator returns lot size
- [ ] News endpoints return articles
- [ ] Trade signal creation works
- [ ] Signal status updates work

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process on port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Database Connection Error
```bash
# Check MongoDB is running
mongod

# Or use MongoDB Atlas - update .env
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net
```

### API Returns 500 Error
```bash
# Check backend logs for error message
# If JWT issue, make sure SECRET_KEY is in .env
```

### CORS Error
```bash
# Backend has CORS enabled
# If still getting error, check request headers
```

---

## 📊 Performance Expectations

- Registration: < 200ms
- Login: < 100ms
- News fetch: < 5s
- Signal creation: < 150ms
- Lot size calculation: < 50ms
- Risk info retrieval: < 100ms

---

**Happy Testing! 🚀**
