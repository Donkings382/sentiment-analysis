import styles from "./TweetCard.module.css";

function TweetCard({ tweet }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m`;
    if (diffHours < 24) return `${diffHours}h`;
    if (diffDays < 7) return `${diffDays}d`;

    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    });
  };

  const getSentimentLabel = (label) => {
    switch (label) {
      case "positive":
        return { text: "Positive", color: "#059669" };
      case "negative":
        return { text: "Negative", color: "#dc2626" };
      default:
        return { text: "Neutral", color: "#2563eb" };
    }
  };

  const formatNumber = (num) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
    if (num >= 1000) return (num / 1000).toFixed(1) + "K";
    return num.toString();
  };

  const sentimentInfo = getSentimentLabel(tweet.sentiment.label);

  return (
    <article className={styles.card}>
      <div className={styles.header}>
        <div className={styles.headerMeta}>
          <span
            className={styles.sentimentBadge}
            style={{
              backgroundColor: sentimentInfo.color + "15",
              color: sentimentInfo.color,
            }}
          >
            {sentimentInfo.text}
          </span>
          <time className={styles.time}>{formatDate(tweet.createdAt)}</time>
        </div>
      </div>

      <p className={styles.text}>{tweet.text}</p>

      <div className={styles.footer}>
        <div className={styles.viewOnXRow}>
          <a 
            href={`https://twitter.com/status/${tweet.id}`} 
            target="_blank" 
            rel="noopener noreferrer"
            className={styles.viewOnX}
          >
            View on
            <svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14">
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
            </svg>
          </a>
        </div>

        <div className={styles.metricsRow}>
          <div className={styles.metrics}>
            <button
              className={styles.metric}
              aria-label={`${tweet.metrics.likes} likes`}
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
              </svg>
              <span>{formatNumber(tweet.metrics.likes)}</span>
            </button>

            <button
              className={styles.metric}
              aria-label={`${tweet.metrics.replies} replies`}
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
              </svg>
              <span>{formatNumber(tweet.metrics.replies)}</span>
            </button>
          </div>

          <div className={styles.confidence}>
            <span className={styles.confidenceLabel}>Score</span>
            <span className={styles.confidenceValue}>
              {Math.round(tweet.sentiment.confidence * 100)}%
            </span>
          </div>
        </div>
      </div>
    </article>
  );
}

export default TweetCard;
