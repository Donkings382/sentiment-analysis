from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from collections import Counter

class SentimentAnalyzer:
    """Sentiment analysis using VADER + TextBlob combined approach with weighted scoring"""
    
    def __init__(self, threshold=0.15, vader_weight=0.7, textblob_weight=0.3):
        """
        Initialize sentiment analyzer
        
        Args:
            threshold: Score threshold for positive/negative classification (default: 0.15)
            vader_weight: Weight for VADER score (default: 0.7 - optimized for social media)
            textblob_weight: Weight for TextBlob score (default: 0.3)
        """
        self.vader = SentimentIntensityAnalyzer()
        self.threshold = threshold
        self.vader_weight = vader_weight
        self.textblob_weight = textblob_weight
    
    def analyze_text(self, text: str) -> dict:
        """Analyze sentiment for a single text with weighted scoring"""
        vader_scores = self.vader.polarity_scores(text)
        vader_compound = vader_scores['compound']
        
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        
        # Weighted combined score (70% VADER, 30% TextBlob by default)
        combined_score = (self.vader_weight * vader_compound) + (self.textblob_weight * textblob_polarity)
        
        if combined_score >= self.threshold:
            sentiment_label = 'Positive'
        elif combined_score <= -self.threshold:
            sentiment_label = 'Negative'
        else:
            sentiment_label = 'Neutral'
        
        return {
            'vader_score': vader_compound,
            'textblob_score': textblob_polarity,
            'combined_score': combined_score,
            'sentiment_label': sentiment_label
        }
    
    def analyze_batch(self, texts: list) -> list:
        """Analyze sentiment for multiple texts"""
        return [self.analyze_text(text) for text in texts]
    
    def generate_summary(self, tweets_data: list) -> dict:
        """
        Generate overall sentiment summary with explanation using average score method
        
        Args:
            tweets_data: List of dicts with 'text', 'sentiment_label', 'combined_score', 'likes', etc.
        
        Returns:
            dict with statistics and explanation
        """
        if not tweets_data:
            return {
                'total': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'positive_percent': 0,
                'negative_percent': 0,
                'neutral_percent': 0,
                'average_score': 0,
                'overall_sentiment': 'Neutral',
                'confidence': 'Low',
                'explanation': 'No tweets to analyze.'
            }
        
        # Count sentiments
        sentiments = [tweet['sentiment_label'] for tweet in tweets_data]
        sentiment_counts = Counter(sentiments)
        
        total = len(tweets_data)
        positive = sentiment_counts.get('Positive', 0)
        negative = sentiment_counts.get('Negative', 0)
        neutral = sentiment_counts.get('Neutral', 0)
        
        positive_percent = round(positive / total * 100, 1)
        negative_percent = round(negative / total * 100, 1)
        neutral_percent = round(neutral / total * 100, 1)
        
        # Calculate average combined score (improved method)
        scores = [tweet['combined_score'] for tweet in tweets_data]
        average_score = sum(scores) / len(scores)
        
        # Determine overall sentiment based on average score
        if average_score >= self.threshold:
            overall_sentiment = 'Positive'
        elif average_score <= -self.threshold:
            overall_sentiment = 'Negative'
        else:
            overall_sentiment = 'Neutral'
        
        # Calculate confidence level based on score distribution
        confidence = self._calculate_confidence(average_score, positive_percent, negative_percent, neutral_percent)
        
        # Generate explanation
        explanation = self._generate_explanation(
            tweets_data, overall_sentiment, average_score, positive_percent, 
            negative_percent, neutral_percent, confidence
        )
        
        return {
            'total': total,
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'positive_percent': positive_percent,
            'negative_percent': negative_percent,
            'neutral_percent': neutral_percent,
            'average_score': round(average_score, 3),
            'overall_sentiment': overall_sentiment,
            'confidence': confidence,
            'explanation': explanation
        }
    
    def _calculate_confidence(self, average_score, positive_percent, negative_percent, neutral_percent):
        """Calculate confidence level based on score distribution"""
        # High confidence: Strong majority (>70%) or high average score (>0.5 or <-0.5)
        max_percent = max(positive_percent, negative_percent, neutral_percent)
        
        if abs(average_score) > 0.5 or max_percent > 70:
            return 'High'
        elif abs(average_score) > 0.25 or max_percent > 50:
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_explanation(self, tweets_data, overall_sentiment, average_score,
                             positive_percent, negative_percent, neutral_percent, confidence):
        """Generate human-readable explanation for sentiment results"""
        
        # Sort tweets by engagement (likes + retweets)
        sorted_tweets = sorted(
            tweets_data, 
            key=lambda x: x.get('likes', 0) + x.get('retweets', 0), 
            reverse=True
        )
        
        # Get top positive and negative tweets
        positive_tweets = [t for t in sorted_tweets if t['sentiment_label'] == 'Positive'][:3]
        negative_tweets = [t for t in sorted_tweets if t['sentiment_label'] == 'Negative'][:3]
        
        # Calculate average engagement
        avg_likes = sum(t.get('likes', 0) for t in tweets_data) / len(tweets_data)
        
        # Build explanation
        explanation_parts = []
        
        # Overall statement with average score
        explanation_parts.append(
            f"Overall sentiment is {overall_sentiment.upper()} (average score: {average_score:.3f}) "
            f"with {confidence.lower()} confidence. "
            f"Distribution: {positive_percent}% positive, {neutral_percent}% neutral, "
            f"and {negative_percent}% negative tweets."
        )
        
        # Confidence explanation
        if confidence == 'High':
            explanation_parts.append(
                f"\n\nHigh confidence indicates strong consensus in sentiment across tweets."
            )
        elif confidence == 'Low':
            explanation_parts.append(
                f"\n\nLow confidence suggests mixed opinions with no clear dominant sentiment."
            )
        
        # Positive analysis
        if positive_tweets:
            top_positive = positive_tweets[0]
            positive_snippet = top_positive['text'][:100] + "..." if len(top_positive['text']) > 100 else top_positive['text']
            explanation_parts.append(
                f"\n\nPositive sentiment ({positive_percent}%) is driven by tweets expressing excitement and support. "
                f"The most engaged positive tweet ('{positive_snippet}') received "
                f"{top_positive.get('likes', 0):,} likes and {top_positive.get('retweets', 0):,} retweets."
            )
        
        # Negative analysis
        if negative_tweets:
            top_negative = negative_tweets[0]
            negative_snippet = top_negative['text'][:100] + "..." if len(top_negative['text']) > 100 else top_negative['text']
            explanation_parts.append(
                f"\n\nNegative sentiment ({negative_percent}%) includes criticism and concerns. "
                f"Top negative tweet: '{negative_snippet}' with "
                f"{top_negative.get('likes', 0):,} likes."
            )
        
        # Neutral analysis (if significant)
        if neutral_percent > 30:
            explanation_parts.append(
                f"\n\nSignificant neutral sentiment ({neutral_percent}%) suggests informational or factual tweets "
                f"without strong emotional tone."
            )
        
        # Engagement insight
        if avg_likes > 10000:
            explanation_parts.append(
                f"\n\nHigh engagement detected with average {avg_likes:,.0f} likes per tweet, "
                f"indicating strong public interest and viral potential."
            )
        elif avg_likes > 1000:
            explanation_parts.append(
                f"\n\nModerate engagement with average {avg_likes:,.0f} likes per tweet, "
                f"showing steady public interest."
            )
        else:
            explanation_parts.append(
                f"\n\nLow engagement with average {avg_likes:,.0f} likes per tweet."
            )
        
        return "".join(explanation_parts)
    