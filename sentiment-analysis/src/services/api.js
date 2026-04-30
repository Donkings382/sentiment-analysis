const API_BASE_URL = 'http://localhost:8000';

export async function searchTweets(query, startDate = null, endDate = null, maxResults = 100) {
  try {
    const body = {
      query: query,
      max_results: maxResults
    };
    
    if (startDate) {
      body.start_date = startDate + 'T00:00:00Z';
    }
    if (endDate) {
      body.end_date = endDate + 'T23:59:59Z';
    }
    
    const response = await fetch(`${API_BASE_URL}/api/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch tweets');
    }
    
    const data = await response.json();
    
    return {
      tweets: data.tweets.map(tweet => ({
        id: tweet.id,
        text: tweet.text,
        author: {
          name: 'Twitter User',
          username: 'user',
          avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${tweet.id}`
        },
        createdAt: tweet.date,
        metrics: {
          likes: tweet.likes,
          retweets: tweet.retweets,
          replies: tweet.replies
        },
        sentiment: {
          score: tweet.combined_score,
          label: tweet.sentiment_label.toLowerCase(),
          confidence: Math.abs(tweet.combined_score)
        }
      })),
      summary: data.summary
    };
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}