import styles from './Header.module.css'

function Header({ onBack, showBack = false }) {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.logo}>
          {showBack && (
            <button className={styles.backButton} onClick={onBack} aria-label="Go back">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M19 12H5M12 19l-7-7 7-7" />
              </svg>
            </button>
          )}
          <svg 
            className={styles.logoIcon} 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2"
          >
            <path d="M12 2L2 7l10 5 10-5-10-5z" />
            <path d="M2 17l10 5 10-5" />
            <path d="M2 12l10 5 10-5" />
          </svg>
          <span className={styles.logoText}>Sentiment Scraper</span>
        </div>
        <p className={styles.tagline}>Search and analyze sentiment</p>
      </div>
    </header>
  )
}

export default Header