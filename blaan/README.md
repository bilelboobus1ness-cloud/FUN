# BLAAN - Trading Signals Platform 🚀

A comprehensive full-stack trading tool that combines real-time forex news, automated trade signal generation, and intelligent risk management. Get signals categorized by currency pair with verified lot sizing and risk calculations.

## Features ✨

- **📰 Market News Integration**: Real-time forex news aggregated and categorized by currency pair
- **📊 Trade Signal Generation**: Automated signals based on news events and market conditions
- **💰 Risk Management**: Intelligent lot size calculation and position sizing
- **📱 Multi-Channel Notifications**: Email, WhatsApp, and Telegram support
- **🔐 Account Management**: Secure trading account setup with risk profiles
- **📈 Dashboard**: Real-time overview of signals and account statistics
- **🎯 Risk Calculator**: Advanced calculator for position sizing and risk/reward analysis

## Tech Stack 🛠️

### Backend
- **Framework**: Flask (Python 3.9+)
- **Database**: MongoDB
- **APIs**: NewsAPI, Twilio (WhatsApp), Telegram Bot API
- **Task Scheduling**: APScheduler

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

## Project Structure 📁

```
blaan/
├── backend/
│   ├── app/
│   │   ├── models/           # Database models
│   │   │   ├── user.py
│   │   │   ├── account.py
│   │   │   └── trade_signal.py
│   │   ├── services/         # Business logic
│   │   │   ├── news_service.py
│   │   │   ├── notification_service.py
│   │   │   └── risk_calculator.py
│   │   ├── routes/           # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── account.py
│   │   │   ├── trades.py
│   │   │   └── news.py
│   │   └── __init__.py
│   ├── main.py               # Flask app entry point
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/       # React components
    │   │   ├── Navbar.jsx
    │   │   ├── Dashboard.jsx
    │   │   ├── TradeSignals.jsx
    │   │   ├── AccountSetup.jsx
    │   │   ├── NewsCenter.jsx
    │   │   └── RiskCalculator.jsx
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── vite.config.js
    └── package.json
```

## Installation & Setup 🚀

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB (local or Atlas)
- NewsAPI key (free at https://newsapi.org)
- Telegram Bot Token (optional)
- Twilio Account (optional, for WhatsApp)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Run Flask server**
   ```bash
   python main.py
   ```
   Server runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   App runs on `http://localhost:5173`

### Environment Variables (.env)

Create a `.env` file in the backend directory:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=blaan_db

# NewsAPI
NEWSAPI_KEY=your_newsapi_key

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# WhatsApp/Twilio (optional)
WHATSAPP_ACCOUNT_SID=your_account_sid
WHATSAPP_AUTH_TOKEN=your_auth_token
WHATSAPP_FROM_NUMBER=whatsapp:+1234567890

# Email
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Flask
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

## API Endpoints 🔌

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Trading Accounts
- `POST /api/account/create` - Create trading account
- `GET /api/account/<user_id>` - Get user accounts
- `PUT /api/account/<account_id>/update-balance` - Update balance
- `PUT /api/account/<account_id>/update-risk` - Update risk percentage
- `GET /api/account/<account_id>/risk-info` - Get risk information

### Trade Signals
- `POST /api/trades/create` - Create trade signal
- `GET /api/trades/all` - Get all signals
- `GET /api/trades/pair/<pair>` - Get signals for pair
- `GET /api/trades/pending` - Get pending signals
- `POST /api/trades/calculate-lot-size` - Calculate lot size
- `PUT /api/trades/<signal_id>/update-status` - Update signal status

### Market News
- `GET /api/news/forex` - Get forex news
- `GET /api/news/categorized` - Get news by currency pair
- `GET /api/news/currency/<code>` - Get news for currency
- `GET /api/news/high-impact` - Get high-impact news

## How to Use 📖

### 1. Register & Setup Account
- Register on the platform
- Add your trading account details
- Set your risk percentage (recommended: 1-2%)

### 2. Monitor News
- Check the "Market News" section for forex updates
- News is automatically categorized by currency pair
- High-impact news is highlighted

### 3. Generate Trade Signals
- Based on news and market conditions, generate signals
- Each signal includes entry, stop loss, and take profit
- Lot size is automatically calculated

### 4. Risk Calculator
- Use the calculator to verify position sizing
- Understand potential profit/loss before trading
- Adjust parameters to match your risk tolerance

### 5. Receive Notifications
- Set notification preferences (Email, WhatsApp, Telegram)
- Get alerts for new trade signals
- Track signal execution in real-time

## Risk Management Best Practices ⚠️

1. **Start Small**: Begin with 1-2% risk per trade
2. **Maintain Ratio**: Always target at least 1:2 Risk:Reward
3. **Use Stop Loss**: Never trade without a defined stop loss
4. **Track Results**: Monitor your win rate and profitability
5. **Scale Gradually**: Increase lot sizes only after consistent profits

## Key Formulas 📐

### Risk Amount
```
Risk Amount = Account Balance × Risk Percentage
```

### Lot Size
```
Lot Size = Risk Amount / (Pip Distance × Pip Value)
```

### Potential Loss
```
Loss = (Entry Price - Stop Loss) × Lot Size × 10000 × Pip Value
```

### Potential Profit
```
Profit = (Take Profit - Entry Price) × Lot Size × 10000 × Pip Value
```

## Deployment 🌐

### Docker Deployment
```bash
docker-compose up -d
```

### Heroku/Cloud Deployment
- Backend: Deploy Flask app to Heroku/Railway/Render
- Frontend: Deploy React to Vercel/Netlify
- Database: Use MongoDB Atlas for cloud MongoDB

## Support & Contribution 🤝

- Report issues via GitHub Issues
- Contribute improvements via Pull Requests
- Follow the existing code style and structure

## License 📄

MIT License - Feel free to use for personal and commercial projects

## Disclaimer ⚖️

**Important**: This tool is for educational purposes. Trading forex carries significant risk. Always do your own research and consult with a financial advisor. Past performance does not guarantee future results.

---

**Built with ❤️ for traders who want smarter signal analysis and risk management.**
