import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './TradeSignals.css'

function TradeSignals({ account }) {
  const [signals, setSignals] = useState([])
  const [filter, setFilter] = useState('all')
  const [selectedPair, setSelectedPair] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchSignals()
  }, [filter])

  const fetchSignals = async () => {
    try {
      setLoading(true)
      let endpoint = '/api/trades/all'
      if (filter === 'pending') {
        endpoint = '/api/trades/pending'
      }
      const response = await axios.get(endpoint)
      setSignals(response.data.signals || response.data.pending_signals || [])
    } catch (error) {
      console.error('Error fetching signals:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchPairSignals = async (pair) => {
    try {
      setLoading(true)
      const response = await axios.get(`/api/trades/pair/${pair}`)
      setSignals(response.data.signals || [])
    } catch (error) {
      console.error('Error fetching pair signals:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePairChange = (e) => {
    const pair = e.target.value
    setSelectedPair(pair)
    if (pair) {
      fetchPairSignals(pair)
    } else {
      fetchSignals()
    }
  }

  const updateSignalStatus = async (signalId, newStatus) => {
    try {
      await axios.put(`/api/trades/${signalId}/update-status`, { status: newStatus })
      fetchSignals()
    } catch (error) {
      console.error('Error updating signal:', error)
    }
  }

  const uniquePairs = [...new Set(signals.map(s => s.currency_pair))]

  return (
    <div className="trade-signals">
      <h2>Trade Signals</h2>

      <div className="filters">
        <div className="filter-group">
          <label>Filter by Status:</label>
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="all">All Signals</option>
            <option value="pending">Pending</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Filter by Pair:</label>
          <select value={selectedPair} onChange={handlePairChange}>
            <option value="">All Pairs</option>
            {uniquePairs.map(pair => (
              <option key={pair} value={pair}>{pair}</option>
            ))}
          </select>
        </div>
      </div>

      {loading && <div className="loading">Loading signals...</div>}

      {!loading && signals.length > 0 ? (
        <div className="signals-container">
          {signals.map((signal) => (
            <div key={signal._id} className="signal-card">
              <div className="signal-header">
                <h3>{signal.currency_pair}</h3>
                <span className={`signal-badge ${signal.signal_type.toLowerCase()}`}>
                  {signal.signal_type}
                </span>
                <span className={`status-badge ${signal.status}`}>
                  {signal.status}
                </span>
              </div>

              <div className="signal-details">
                <div className="detail-row">
                  <span>Entry Price:</span>
                  <strong>{signal.entry_price.toFixed(5)}</strong>
                </div>
                <div className="detail-row">
                  <span>Stop Loss:</span>
                  <strong>{signal.stop_loss.toFixed(5)}</strong>
                </div>
                <div className="detail-row">
                  <span>Take Profit:</span>
                  <strong>{signal.take_profit.toFixed(5)}</strong>
                </div>
                <div className="detail-row">
                  <span>Lot Size:</span>
                  <strong>{signal.lot_size}</strong>
                </div>
                <div className="detail-row">
                  <span>Risk Amount:</span>
                  <strong className="risk-amount">${signal.risk_amount.toFixed(2)}</strong>
                </div>
                <div className="detail-row">
                  <span>Execution Time:</span>
                  <strong>{signal.execution_time}</strong>
                </div>
                <div className="detail-row">
                  <span>News Source:</span>
                  <strong>{signal.news_source}</strong>
                </div>
              </div>

              {signal.status === 'pending' && (
                <div className="signal-actions">
                  <button 
                    onClick={() => updateSignalStatus(signal._id, 'executed')}
                    className="btn btn-success"
                  >
                    Execute
                  </button>
                  <button 
                    onClick={() => updateSignalStatus(signal._id, 'cancelled')}
                    className="btn btn-danger"
                  >
                    Cancel
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        !loading && <p className="no-data">No trade signals available.</p>
      )}
    </div>
  )
}

export default TradeSignals
