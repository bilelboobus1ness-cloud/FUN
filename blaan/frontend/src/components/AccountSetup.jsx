import React, { useState } from 'react'
import axios from 'axios'
import './AccountSetup.css'

function AccountSetup({ user, onAccountCreated }) {
  const [formData, setFormData] = useState({
    broker_name: '',
    account_number: '',
    api_key: '',
    balance: '',
    currency: 'USD',
    leverage: '1',
    risk_percentage: '2'
  })

  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      // For demo purposes, using a mock user ID
      const mockUserId = user?.user_id || 'demo-user-' + Date.now()

      const response = await axios.post('/api/account/create', {
        user_id: mockUserId,
        ...formData,
        balance: parseFloat(formData.balance),
        leverage: parseInt(formData.leverage),
        risk_percentage: parseFloat(formData.risk_percentage)
      })

      // Fetch account details
      const accountRes = await axios.get(`/api/account/${response.data.account_id}`)
      
      // Store account in localStorage
      localStorage.setItem('account', JSON.stringify(accountRes.data))
      onAccountCreated(accountRes.data)

      setMessage('Account created successfully!')
      setFormData({
        broker_name: '',
        account_number: '',
        api_key: '',
        balance: '',
        currency: 'USD',
        leverage: '1',
        risk_percentage: '2'
      })

      setTimeout(() => setMessage(''), 3000)
    } catch (error) {
      setMessage('Error creating account: ' + (error.response?.data?.error || error.message))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="account-setup">
      <h2>Trading Account Setup</h2>
      <p>Add your trading account information to calculate lot sizes and risk management</p>

      {message && (
        <div className={`alert ${message.includes('Error') ? 'alert-danger' : 'alert-success'}`}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="setup-form">
        <div className="form-row">
          <div className="form-group">
            <label>Broker Name *</label>
            <input
              type="text"
              name="broker_name"
              value={formData.broker_name}
              onChange={handleChange}
              placeholder="e.g., Forex.com, Interactive Brokers"
              required
            />
          </div>

          <div className="form-group">
            <label>Account Number *</label>
            <input
              type="text"
              name="account_number"
              value={formData.account_number}
              onChange={handleChange}
              placeholder="Your trading account number"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>API Key</label>
            <input
              type="password"
              name="api_key"
              value={formData.api_key}
              onChange={handleChange}
              placeholder="API Key (optional for automation)"
            />
          </div>

          <div className="form-group">
            <label>Account Balance *</label>
            <input
              type="number"
              name="balance"
              value={formData.balance}
              onChange={handleChange}
              placeholder="e.g., 10000"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Currency</label>
            <select name="currency" value={formData.currency} onChange={handleChange}>
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
              <option value="GBP">GBP</option>
              <option value="JPY">JPY</option>
            </select>
          </div>

          <div className="form-group">
            <label>Leverage</label>
            <select name="leverage" value={formData.leverage} onChange={handleChange}>
              <option value="1">1:1</option>
              <option value="10">1:10</option>
              <option value="50">1:50</option>
              <option value="100">1:100</option>
              <option value="200">1:200</option>
            </select>
          </div>

          <div className="form-group">
            <label>Risk Per Trade (%)</label>
            <input
              type="number"
              name="risk_percentage"
              value={formData.risk_percentage}
              onChange={handleChange}
              placeholder="Default: 2"
              step="0.5"
              min="0.1"
              max="10"
            />
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>

      <div className="info-box">
        <h3>💡 Why Risk Management Matters</h3>
        <ul>
          <li><strong>Risk Per Trade:</strong> The percentage of your account balance you're willing to risk on a single trade</li>
          <li><strong>Lot Size:</strong> Automatically calculated based on risk, entry, and stop-loss levels</li>
          <li><strong>Best Practice:</strong> Start with 1-2% risk per trade for long-term profitability</li>
          <li><strong>Leverage:</strong> Higher leverage increases both potential profits and losses</li>
        </ul>
      </div>
    </div>
  )
}

export default AccountSetup
