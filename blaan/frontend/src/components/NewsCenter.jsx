import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './NewsCenter.css'

function NewsCenter() {
  const [newsData, setNewsData] = useState(null)
  const [categorizedNews, setCategorizedNews] = useState({})
  const [highImpactNews, setHighImpactNews] = useState([])
  const [activeTab, setActiveTab] = useState('categorized')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchNewsData()
  }, [])

  const fetchNewsData = async () => {
    try {
      setLoading(true)

      // Fetch categorized news
      const categorizedRes = await axios.get('/api/news/categorized')
      setCategorizedNews(categorizedRes.data.categorized_news || {})

      // Fetch high impact news
      const highImpactRes = await axios.get('/api/news/high-impact')
      setHighImpactNews(highImpactRes.data.high_impact_articles || [])
    } catch (error) {
      console.error('Error fetching news:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="news-center">
      <h2>Market News Center</h2>
      <p>Stay updated with forex trading news categorized by currency pair</p>

      <div className="news-tabs">
        <button
          className={`tab-btn ${activeTab === 'categorized' ? 'active' : ''}`}
          onClick={() => setActiveTab('categorized')}
        >
          📊 By Currency Pair
        </button>
        <button
          className={`tab-btn ${activeTab === 'high-impact' ? 'active' : ''}`}
          onClick={() => setActiveTab('high-impact')}
        >
          ⚡ High Impact
        </button>
        <button
          onClick={fetchNewsData}
          className="tab-btn refresh-btn"
        >
          🔄 Refresh
        </button>
      </div>

      {loading && <div className="loading">Loading news...</div>}

      {!loading && activeTab === 'categorized' && (
        <div className="news-sections">
          {Object.keys(categorizedNews).length > 0 ? (
            Object.entries(categorizedNews).map(([currency, articles]) => (
              <div key={currency} className="currency-section">
                <h3 className="currency-header">{currency}</h3>
                <div className="articles-list">
                  {articles.slice(0, 5).map((article, index) => (
                    <div key={index} className="article-card">
                      {article.image && (
                        <img src={article.image} alt="" className="article-image" />
                      )}
                      <div className="article-content">
                        <h4>{article.title}</h4>
                        <p className="article-description">{article.description}</p>
                        <div className="article-meta">
                          <span className="source">{article.source.name}</span>
                          <span className="date">{formatDate(article.publishedAt)}</span>
                        </div>
                        <a href={article.url} target="_blank" rel="noopener noreferrer" className="read-more">
                          Read Full Article →
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))
          ) : (
            <p className="no-data">No news available for any currency pairs.</p>
          )}
        </div>
      )}

      {!loading && activeTab === 'high-impact' && (
        <div className="articles-list">
          {highImpactNews.length > 0 ? (
            highImpactNews.slice(0, 10).map((article, index) => (
              <div key={index} className="article-card highlight">
                {article.image && (
                  <img src={article.image} alt="" className="article-image" />
                )}
                <div className="article-content">
                  <span className="high-impact-badge">⚡ HIGH IMPACT</span>
                  <h4>{article.title}</h4>
                  <p className="article-description">{article.description}</p>
                  <div className="article-meta">
                    <span className="source">{article.source.name}</span>
                    <span className="date">{formatDate(article.publishedAt)}</span>
                  </div>
                  <a href={article.url} target="_blank" rel="noopener noreferrer" className="read-more">
                    Read Full Article →
                  </a>
                </div>
              </div>
            ))
          ) : (
            <p className="no-data">No high-impact news available.</p>
          )}
        </div>
      )}
    </div>
  )
}

export default NewsCenter
