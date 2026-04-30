import styles from './EmptyState.module.css'

function EmptyState({ message = 'Search for entries to analyze sentiment' }) {
  return (
    <div className={styles.container}>
      <div className={styles.icon}>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M12 2L2 7l10 5 10-5-10-5z" />
          <path d="M2 17l10 5 10-5" />
          <path d="M2 12l10 5 10-5" />
        </svg>
      </div>
      <h3 className={styles.title}>No results yet</h3>
      <p className={styles.message}>{message}</p>
    </div>
  )
}

export default EmptyState