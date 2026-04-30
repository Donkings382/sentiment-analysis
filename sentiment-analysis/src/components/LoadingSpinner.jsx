import styles from './LoadingSpinner.module.css'

function LoadingSpinner() {
  return (
    <div className={styles.container}>
      <div className={styles.spinner}>
        <svg viewBox="0 0 50 50">
          <circle 
            cx="25" 
            cy="25" 
            r="20" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="4"
            strokeLinecap="round"
            strokeDasharray="80 40"
          />
        </svg>
      </div>
      <p className={styles.text}>Searching entries...</p>
    </div>
  )
}

export default LoadingSpinner