import { useState } from 'react'
import styles from './LandingPage.module.css'

function LandingPage({ onSearch }) {
  const [searchVisible, setSearchVisible] = useState(false)
  const [query, setQuery] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [maxResults, setMaxResults] = useState('100')
  const [showWarning, setShowWarning] = useState(false)

  const handleStartSearch = () => {
    setSearchVisible(true)
  }

  const handleMaxResultsChange = (value) => {
    setMaxResults(value)
    if (parseInt(value) >= 500) {
      setShowWarning(true)
    } else {
      setShowWarning(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query.trim(), startDate, endDate, parseInt(maxResults))
    }
  }

  const interestingTopics = [
    'artificial intelligence',
    'climate change',
    'cryptocurrency',
    'electric vehicles'
  ]

  return (
    <div className={styles.container}>
      <div className={styles.profileSection}>
        <div className={styles.avatarContainer}>
          <img 
            src="https://api.dicebear.com/7.x/notionists/svg?seed=Felix&backgroundColor=b6e3f4" 
            alt="AI Assistant Avatar"
            className={styles.avatarImage}
          />
        </div>
      </div>

      <h1 className={styles.title}>Sentiment Analyzer</h1>
      <p className={styles.subtitle}>
        Discover public opinion on any topic with AI-powered sentiment analysis
      </p>

      <div className={`${styles.searchSection} ${searchVisible ? styles.visible : ''}`}>
        <form className={styles.searchForm} onSubmit={handleSubmit}>
          <input
            type="text"
            className={styles.searchInput}
            placeholder="Search for entries... (e.g., AI, crypto, climate)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
          />
          
          <div className={styles.dateFilters}>
            <div className={styles.dateInput}>
              <label htmlFor="landingStartDate">Start Date</label>
              <input
                id="landingStartDate"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>
            <div className={styles.dateInput}>
              <label htmlFor="landingEndDate">End Date</label>
              <input
                id="landingEndDate"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
          </div>
          
          <div className={styles.maxResultsSection}>
            <label htmlFor="maxResults" className={styles.maxResultsLabel}>Max Results</label>
            <select
              id="maxResults"
              value={maxResults}
              onChange={(e) => handleMaxResultsChange(e.target.value)}
              className={styles.maxResultsSelect}
            >
              <option value="50">50 tweets</option>
              <option value="100">100 tweets</option>
              <option value="500">500 tweets</option>
              <option value="1000">1000 tweets</option>
            </select>
            {showWarning && (
              <p className={styles.warning}>
                ⚠️ High volume may take longer and consume more API credits
              </p>
            )}
          </div>
          
          <button 
            type="submit" 
            className={styles.searchButton}
            disabled={!query.trim()}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
            Search
          </button>
        </form>
      </div>

      {!searchVisible && (
        <button className={styles.startButton} onClick={handleStartSearch}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
          Start Searching
        </button>
      )}

      <div className={styles.interestingSection}>
        <p className={styles.interestingLabel}>Explore interesting topics</p>
        <div className={styles.topicsGrid}>
          {interestingTopics.map((topic) => (
            <button 
              key={topic}
              className={styles.topicButton}
              onClick={() => {
                setQuery(topic)
                if (!searchVisible) setSearchVisible(true)
                setTimeout(() => onSearch(topic, '', '', 100), 100)
              }}
            >
              <span className={styles.topicHash}>#</span>
              {topic}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default LandingPage