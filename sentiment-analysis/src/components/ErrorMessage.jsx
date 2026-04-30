import styles from './ErrorMessage.module.css'

function ErrorMessage({ message, onRetry }) {
  return (
    <div className={styles.container}>
      <div className={styles.icon}>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10" />
          <path d="M15 9l-6 6M9 9l6 6" />
        </svg>
      </div>
      <div className={styles.content}>
        <h3 className={styles.title}>Search failed</h3>
        <p className={styles.message}>{message}</p>
      </div>
      {onRetry && (
        <button className={styles.retryButton} onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  )
}

export default ErrorMessage