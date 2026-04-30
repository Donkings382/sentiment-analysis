import TweetCard from './TweetCard'
import SentimentSummary from './SentimentSummary'
import styles from './TweetList.module.css'

function TweetList({ tweets, query, summary }) {
  const sentimentCounts = tweets.reduce((acc, tweet) => {
    acc[tweet.sentiment.label] = (acc[tweet.sentiment.label] || 0) + 1
    return acc
  }, {})

  const avgSentimentScore = tweets.reduce((sum, tweet) => sum + tweet.sentiment.score, 0) / tweets.length

  return (
    <div className={styles.container}>
      <SentimentSummary 
        total={tweets.length}
        positive={sentimentCounts.positive || 0}
        negative={sentimentCounts.negative || 0}
        neutral={sentimentCounts.neutral || 0}
        avgScore={avgSentimentScore}
        explanation={summary?.explanation}
      />
      
      <div className={styles.list}>
        {tweets.map((tweet) => (
          <TweetCard key={tweet.id} tweet={tweet} />
        ))}
      </div>
    </div>
  )
}

export default TweetList