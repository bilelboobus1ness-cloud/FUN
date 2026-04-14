import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './Dashboard.css'

function Dashboard({ user, account }) {
  const [stats, setStats] = useState(null)
  const [recentSignals, setRecentSignals] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true)
        
        // Fetch recent signals
        const signalsRes = await axios.get('/api/trades/all')
        setRecentSignals(signalsRes.data.signals.slice(0, 5))

        // Calculate stats
        const totalSignals = signalsRes.data.signals.length
        const buySignals = signalsRes.data.signals.filter(s => s.signal_type === 'BUY').length
        const sellSignals = signalsRes.data.signals.filter(s => s.signal_type === 'SELL').length
        
        setStats({
          totalSignals,
          buySignals,
          sellSignals,
          accountBalance: account?.current_balance || 0,
          riskPerTrade: account?.risk_percentage || 2
        })
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardData()
  }, [account])

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  return (
    <div className="dashboard">
      <h2>Welcome to BLAAN Trading Platform</h2>
      
      {user && <p className="greeting">Hello, {user.full_name}! 👋</p>}

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>Total Signals</h3>
            <p className="stat-value">{stats?.totalSignals || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-content">
            <h3>Buy Signals</h3>
            <p className="stat-value buy">{stats?.buySignals || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📉</div>
          <div className="stat-content">
            <h3>Sell Signals</h3>
            <p className="stat-value sell">{stats?.sellSignals || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💰</div>
          <div className="stat-content">
            <h3>Account Balance</h3>
            <p className="stat-value">${stats?.accountBalance.toFixed(2) || '0.00'}</p>
          </div>
        </div>
      </div>

      <div className="recent-signals">
        <h3>Recent Trade Signals</h3>
        {recentSignals.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Pair</th>
                <th>Type</th>
                <th>Entry</th>
                <th>SL</th>
                <th>TP</th>
                <th>Lot Size</th>
                <th>Risk</th>
              </tr>
            </thead>
            <tbody>
              {recentSignals.map((signal) => (
                <tr key={signal._id}>
                  <td><strong>{signal.currency_pair}</strong></td>
                  <td>
                    <span className={`signal-badge ${signal.signal_type.toLowerCase()}`}>
                      {signal.signal_type}
                    </span>
                  </td>
                  <td>{signal.entry_price.toFixed(5)}</td>
                  <td>{signal.stop_loss.toFixed(5)}</td>
                  <td>{signal.take_profit.toFixed(5)}</td>
                  <td>{signal.lot_size}</td>
                  <td>${signal.risk_amount.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="no-data">No signals yet. Check the Market News to generate signals!</p>
        )}
      </div>

      <div className="info-section">
        <h3>Quick Start Guide</h3>
        <div className="info-grid">
          <div className="info-card">
            <h4>1. Set Up Your Account</h4>
            <p>Add your trading account information to get started with risk calculations and signal generation.</p>
          </div>
          <div className="info-card">
            <h4>2. Monitor Market News</h4>
            <p>Check the Market News section for forex trading updates categorized by currency pair.</p>
          </div>
          <div className="info-card">
            <h4>3. Generate Signals</h4>
            <p>Based on news and market conditions, generate trade signals with automated risk calculations.</p>
          </div>
          <div className="info-card">
            <h4>4. Execute Trades</h4>
            <p>Execute signals with proper lot sizing and receive notifications via Email, WhatsApp, or Telegram.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
