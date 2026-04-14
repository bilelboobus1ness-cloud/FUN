import React, { useState, useEffect } from 'react'
import './App.css'
import Navbar from './components/Navbar'
import Dashboard from './components/Dashboard'
import TradeSignals from './components/TradeSignals'
import AccountSetup from './components/AccountSetup'
import NewsCenter from './components/NewsCenter'
import RiskCalculator from './components/RiskCalculator'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [user, setUser] = useState(null)
  const [account, setAccount] = useState(null)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    const storedAccount = localStorage.getItem('account')
    if (storedUser) setUser(JSON.parse(storedUser))
    if (storedAccount) setAccount(JSON.parse(storedAccount))
  }, [])

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard user={user} account={account} />
      case 'signals':
        return <TradeSignals account={account} />
      case 'account':
        return <AccountSetup user={user} onAccountCreated={setAccount} />
      case 'news':
        return <NewsCenter />
      case 'calculator':
        return <RiskCalculator account={account} />
      default:
        return <Dashboard user={user} account={account} />
    }
  }

  return (
    <div className="app-container">
      <Navbar 
        user={user} 
        setUser={setUser} 
        currentPage={currentPage} 
        setCurrentPage={setCurrentPage}
        setAccount={setAccount}
      />
      <main className="main-content">
        <div className="container">
          {renderPage()}
        </div>
      </main>
    </div>
  )
}

export default App
