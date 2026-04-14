import React, { useState } from 'react'
import './Navbar.css'

function Navbar({ user, setUser, currentPage, setCurrentPage, setAccount }) {
  const [showDropdown, setShowDropdown] = useState(false)

  const handleLogout = () => {
    localStorage.removeItem('user')
    localStorage.removeItem('account')
    setUser(null)
    setAccount(null)
    setCurrentPage('dashboard')
    setShowDropdown(false)
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="logo">
          <h1>🚀 BLAAN</h1>
          <p>Trading Signals Platform</p>
        </div>
        
        <ul className="nav-links">
          <li><a onClick={() => setCurrentPage('dashboard')} className={currentPage === 'dashboard' ? 'active' : ''}>Dashboard</a></li>
          <li><a onClick={() => setCurrentPage('signals')} className={currentPage === 'signals' ? 'active' : ''}>Trade Signals</a></li>
          <li><a onClick={() => setCurrentPage('news')} className={currentPage === 'news' ? 'active' : ''}>Market News</a></li>
          <li><a onClick={() => setCurrentPage('calculator')} className={currentPage === 'calculator' ? 'active' : ''}>Risk Calculator</a></li>
          <li><a onClick={() => setCurrentPage('account')} className={currentPage === 'account' ? 'active' : ''}>Account Setup</a></li>
        </ul>

        <div className="user-menu">
          {user ? (
            <div className="user-dropdown">
              <button onClick={() => setShowDropdown(!showDropdown)} className="user-btn">
                👤 {user.full_name}
              </button>
              {showDropdown && (
                <div className="dropdown-menu">
                  <a onClick={() => { setCurrentPage('account'); setShowDropdown(false); }}>My Account</a>
                  <a onClick={handleLogout}>Logout</a>
                </div>
              )}
            </div>
          ) : (
            <button className="login-btn">Login</button>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
