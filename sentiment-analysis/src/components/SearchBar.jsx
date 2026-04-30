import { useState, useRef, useEffect } from 'react'
import styles from './SearchBar.module.css'

function SearchBar({ onSearch, initialValue = '', onClear, isLoading }) {
  const [query, setQuery] = useState(initialValue)
  const inputRef = useRef(null)

  useEffect(() => {
    setQuery(initialValue)
  }, [initialValue])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim() && !isLoading) {
      onSearch(query.trim())
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      setQuery('')
      inputRef.current?.blur()
    }
  }

  const handleClear = () => {
    setQuery('')
    if (onClear) onClear()
    inputRef.current?.focus()
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <div className={styles.inputWrapper}>
        <svg 
          className={styles.searchIcon} 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          strokeWidth="2"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="M21 21l-4.35-4.35" />
        </svg>
        
        <input
          ref={inputRef}
          type="text"
          className={styles.input}
          placeholder="Search for entries... (e.g., climate change, AI, crypto)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          aria-label="Search entries"
        />
        
        {query && (
          <button
            type="button"
            className={styles.clearButton}
            onClick={handleClear}
            disabled={isLoading}
            aria-label="Clear search"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 6L6 18M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
      
      <button 
        type="submit" 
        className={styles.submitButton}
        disabled={isLoading || !query.trim()}
        aria-label="Search"
      >
        {isLoading ? (
          <svg className={styles.spinner} viewBox="0 0 24 24" fill="none">
            <circle 
              cx="12" cy="12" r="10" 
              stroke="currentColor" 
              strokeWidth="3" 
              strokeLinecap="round"
              strokeDasharray="31.4 31.4"
            />
          </svg>
        ) : (
          <span>Search</span>
        )}
      </button>
    </form>
  )
}

export default SearchBar