import React, { useState } from 'react'
import axios from 'axios'
import './RiskCalculator.css'

function RiskCalculator({ account }) {
  const [inputs, setInputs] = useState({
    account_balance: account?.current_balance || 10000,
    risk_percentage: 2,
    entry_price: 1.0850,
    stop_loss: 1.0800,
    take_profit: 1.0950,
    pip_value: 10
  })

  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setInputs(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const calculateLotSize = async () => {
    try {
      setLoading(true)
      const response = await axios.post('/api/trades/calculate-lot-size', {
        account_balance: parseFloat(inputs.account_balance),
        risk_percentage: parseFloat(inputs.risk_percentage),
        entry_price: parseFloat(inputs.entry_price),
        stop_loss: parseFloat(inputs.stop_loss),
        take_profit: parseFloat(inputs.take_profit),
        pip_value: parseInt(inputs.pip_value)
      })

      setResult(response.data)
    } catch (error) {
      console.error('Error calculating lot size:', error)
    } finally {
      setLoading(false)
    }
  }

  const resetCalculator = () => {
    setInputs({
      account_balance: account?.current_balance || 10000,
      risk_percentage: 2,
      entry_price: 1.0850,
      stop_loss: 1.0800,
      take_profit: 1.0950,
      pip_value: 10
    })
    setResult(null)
  }

  return (
    <div className="risk-calculator">
      <h2>Risk Management Calculator</h2>
      <p>Calculate optimal lot size and manage your trading risk</p>

      <div className="calculator-grid">
        <div className="calculator-form">
          <h3>Input Parameters</h3>

          <div className="form-group">
            <label>Account Balance ($)</label>
            <input
              type="number"
              name="account_balance"
              value={inputs.account_balance}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Risk Per Trade (%)</label>
            <input
              type="number"
              name="risk_percentage"
              value={inputs.risk_percentage}
              onChange={handleChange}
              step="0.5"
              min="0.1"
              max="10"
            />
          </div>

          <div className="form-group">
            <label>Entry Price</label>
            <input
              type="number"
              name="entry_price"
              value={inputs.entry_price}
              onChange={handleChange}
              step="0.0001"
            />
          </div>

          <div className="form-group">
            <label>Stop Loss Price</label>
            <input
              type="number"
              name="stop_loss"
              value={inputs.stop_loss}
              onChange={handleChange}
              step="0.0001"
            />
          </div>

          <div className="form-group">
            <label>Take Profit Price</label>
            <input
              type="number"
              name="take_profit"
              value={inputs.take_profit}
              onChange={handleChange}
              step="0.0001"
            />
          </div>

          <div className="form-group">
            <label>Pip Value</label>
            <input
              type="number"
              name="pip_value"
              value={inputs.pip_value}
              onChange={handleChange}
            />
          </div>

          <div className="button-group">
            <button onClick={calculateLotSize} className="btn btn-primary" disabled={loading}>
              {loading ? 'Calculating...' : 'Calculate'}
            </button>
            <button onClick={resetCalculator} className="btn btn-secondary">
              Reset
            </button>
          </div>
        </div>

        <div className="calculator-results">
          <h3>Results</h3>
          {result ? (
            <div className="results-display">
              <div className="result-card">
                <h4>Lot Size</h4>
                <p className="result-value">{result.lot_size}</p>
                <p className="result-unit">lots</p>
              </div>

              <div className="result-card">
                <h4>Maximum Risk</h4>
                <p className="result-value">${result.potential_loss}</p>
                <p className="result-unit">per trade</p>
              </div>

              <div className="result-card">
                <h4>Potential Profit</h4>
                <p className="result-value positive">${result.potential_profit}</p>
                <p className="result-unit">if TP hit</p>
              </div>

              <div className="result-card">
                <h4>Risk:Reward Ratio</h4>
                <p className="result-value">{result.reward_risk_ratio}:1</p>
                <p className="result-unit">target</p>
              </div>

              <div className="info-note">
                <p><strong>💡 Tip:</strong> Aim for Risk:Reward ratio of at least 1:2 for profitable trading</p>
              </div>
            </div>
          ) : (
            <div className="no-results">
              <p>Enter your parameters and click Calculate to see results</p>
            </div>
          )}
        </div>
      </div>

      <div className="formula-section">
        <h3>How It Works</h3>
        <div className="formulas">
          <div className="formula-card">
            <h4>Risk Amount</h4>
            <p>Risk Amount = Account Balance × Risk %</p>
            <p className="example">Example: $10,000 × 2% = $200</p>
          </div>

          <div className="formula-card">
            <h4>Lot Size</h4>
            <p>Lot Size = Risk Amount / (Pips Distance × Pip Value)</p>
            <p className="example">Example: $200 / (50 pips × $10) = 0.4 lots</p>
          </div>

          <div className="formula-card">
            <h4>Potential Loss</h4>
            <p>Loss = (Entry - SL) × Lot Size × 10000 × Pip Value</p>
            <p className="example">Equals your risk per trade</p>
          </div>

          <div className="formula-card">
            <h4>Potential Profit</h4>
            <p>Profit = (TP - Entry) × Lot Size × 10000 × Pip Value</p>
            <p className="example">Maximum profit if take profit is hit</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RiskCalculator
