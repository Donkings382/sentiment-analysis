import { useState, useCallback } from 'react'
import Header from './components/Header'
import SearchBar from './components/SearchBar'
import TweetList from './components/TweetList'
import LoadingSpinner from './components/LoadingSpinner'
import ErrorMessage from './components/ErrorMessage'
import LandingPage from './components/LandingPage'
import { searchTweets } from './services/api'
import styles from './App.module.css'

function App() {
  const [searchQuery, setSearchQuery] = useState('')
  const [tweets, setTweets] = useState([])
  const [summary, setSummary] = useState(null)
  const [searchDates, setSearchDates] = useState({ start: '', end: '' })
  const [searchMaxResults, setSearchMaxResults] = useState(100)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [hasSearched, setHasSearched] = useState(false)
  const [showLanding, setShowLanding] = useState(true)

  const handleSearch = useCallback(async (query, startDate = '', endDate = '', maxResults = 100) => {
    if (!query.trim()) return

    setShowLanding(false)
    setSearchQuery(query)
    setSearchDates({ start: startDate, end: endDate })
    setSearchMaxResults(maxResults)
    setIsLoading(true)
    setError(null)
    setHasSearched(true)
    setTweets([])
    setSummary(null)

    try {
      const results = await searchTweets(query, startDate, endDate, maxResults)
      setTweets(results.tweets)
      setSummary(results.summary)
    } catch (err) {
      setError(err.message || 'An error occurred while searching')
    } finally {
      setIsLoading(false)
    }
  }, [])

  const handleBackToLanding = useCallback(() => {
    setSearchQuery('')
    setTweets([])
    setSummary(null)
    setError(null)
    setHasSearched(false)
    setShowLanding(true)
  }, [])

  if (showLanding) {
    return (
      <div className={styles.app}>
        <Header onBack={handleBackToLanding} showBack={false} />
        <main className={styles.main}>
          <LandingPage onSearch={handleSearch} />
        </main>
      </div>
    )
  }

  return (
    <div className={styles.app}>
      <Header onBack={handleBackToLanding} showBack={hasSearched && !isLoading} />
      <main className={styles.main}>
        <div className={styles.container}>
          <SearchBar 
            onSearch={(query) => handleSearch(query, searchDates.start, searchDates.end, searchMaxResults)} 
            initialValue={searchQuery}
            onClear={handleBackToLanding}
            isLoading={isLoading}
          />
          
          {isLoading && <LoadingSpinner />}
          
          {error && <ErrorMessage message={error} onRetry={() => handleSearch(searchQuery)} />}
          
          {!isLoading && !error && hasSearched && tweets.length === 0 && (
            <div className={styles.emptyState}>
              <p>No entries found for your search</p>
            </div>
          )}
          
          {!isLoading && !error && tweets.length > 0 && (
            <TweetList tweets={tweets} query={searchQuery} summary={summary} />
          )}
        </div>
      </main>
    </div>
  )
}

export default App