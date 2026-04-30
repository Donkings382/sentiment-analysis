import styles from './SentimentSummary.module.css'

function SentimentSummary({ total, positive, negative, neutral, avgScore, explanation }) {
  const getOverallSentiment = () => {
    if (avgScore > 0.15) return { label: 'Positive', color: '#059669' }
    if (avgScore < -0.15) return { label: 'Negative', color: '#dc2626' }
    return { label: 'Neutral', color: '#6b7280' }
  }

  const overallSentiment = getOverallSentiment()
  const positivePercent = total > 0 ? (positive / total * 100).toFixed(0) : 0
  const negativePercent = total > 0 ? (negative / total * 100).toFixed(0) : 0
  const neutralPercent = total > 0 ? (neutral / total * 100).toFixed(0) : 0

  const getHighestSentiment = () => {
    const percentages = {
      positive: parseFloat(positivePercent),
      negative: parseFloat(negativePercent),
      neutral: parseFloat(neutralPercent)
    }
    const highest = Object.keys(percentages).reduce((a, b) => percentages[a] > percentages[b] ? a : b)
    return {
      type: highest,
      percentage: percentages[highest]
    }
  }

  const highestSentiment = getHighestSentiment()

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.title}>Sentiment Analysis</h2>
        <span className={styles.overallBadge} style={{ backgroundColor: overallSentiment.color + '15', color: overallSentiment.color }}>
          Overall: {overallSentiment.label}
        </span>
      </div>

      <div className={styles.stats}>
        <div className={styles.statItem}>
          <span className={styles.statValue}>{total}</span>
          <span className={styles.statLabel}>Total Entries</span>
        </div>
        
        <div className={styles.barContainer}>
          <div className={styles.bar}>
            <div 
              className={styles.barPositive} 
              style={{ width: `${positivePercent}%` }}
              aria-label={`${positivePercent}% positive`}
            />
            <div 
              className={styles.barNeutral} 
              style={{ width: `${neutralPercent}%` }}
              aria-label={`${neutralPercent}% neutral`}
            />
            <div 
              className={styles.barNegative} 
              style={{ width: `${negativePercent}%` }}
              aria-label={`${negativePercent}% negative`}
            />
          </div>
          <div className={styles.barLabels}>
            <span className={styles.barLabelPositive}>Positive {positivePercent}%</span>
            <span className={styles.barLabelNeutral}>Neutral {neutralPercent}%</span>
            <span className={styles.barLabelNegative}>Negative {negativePercent}%</span>
          </div>
        </div>
      </div>

      <div className={styles.secondaryDisplay}>
        <div className={styles.prominentSentiment}>
          <span className={styles.prominentLabel}>
            <span className={`${styles.prominentPercentage} ${styles[`prominentPercentage${highestSentiment.type.charAt(0).toUpperCase() + highestSentiment.type.slice(1)}`]}`}>
              {highestSentiment.percentage}%
            </span> {highestSentiment.type.charAt(0).toUpperCase() + highestSentiment.type.slice(1)} sentiment
          </span>
        </div>
        {explanation && (
          <p className={styles.sentimentDescription}>
            {explanation}
          </p>
        )}
      </div>
    </div>
  )
}

export default SentimentSummary