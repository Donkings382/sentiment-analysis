from sqlalchemy.orm import Session
from models.database import Search, Tweet
from datetime import datetime
from typing import List, Optional, Dict

class DatabaseService:
    """Service layer for database operations"""
    
    @staticmethod
    def create_search(db: Session, query: str, start_date: str = None, 
                     end_date: str = None) -> Search:
        """Create a new search record"""
        search = Search(
            query=query,
            start_date=start_date,
            end_date=end_date,
            created_at=datetime.utcnow()
        )
        db.add(search)
        db.commit()
        db.refresh(search)
        return search
    
    @staticmethod
    def create_tweets_bulk(db: Session, search_id: int, tweets_data: List[dict]) -> List[Tweet]:
        """Create multiple tweets linked to a search"""
        tweets = []
        for data in tweets_data:
            tweet = Tweet(
                search_id=search_id,
                tweet_id=data.get('id', ''),
                text=data.get('text', ''),
                date=data.get('date'),
                likes=data.get('likes', 0),
                replies=data.get('replies', 0),
                retweets=data.get('retweets', 0),
                url=data.get('url'),
                vader_score=data.get('vader_score'),
                textblob_score=data.get('textblob_score'),
                combined_score=data.get('combined_score'),
                sentiment_label=data.get('sentiment_label')
            )
            tweets.append(tweet)
        
        db.bulk_save_objects(tweets)
        db.commit()
        return tweets
    
    @staticmethod
    def update_search_summary(db: Session, search_id: int, summary: Dict) -> Search:
        """Update search with sentiment summary"""
        search = db.query(Search).filter(Search.id == search_id).first()
        if search:
            search.total_tweets = summary.get('total', 0)
            search.positive_count = summary.get('positive', 0)
            search.neutral_count = summary.get('neutral', 0)
            search.negative_count = summary.get('negative', 0)
            search.average_sentiment = summary.get('average_score', 0)
            search.explanation = summary.get('explanation', '')
            db.commit()
            db.refresh(search)
        return search
    
    @staticmethod
    def get_latest_search_by_query(db: Session, query: str) -> Optional[Search]:
        """Get the most recent search for a query"""
        return db.query(Search).filter(Search.query == query).order_by(Search.created_at.desc()).first()
    
    @staticmethod
    def get_tweets_by_search_id(db: Session, search_id: int) -> List[Tweet]:
        """Get all tweets for a specific search"""
        return db.query(Tweet).filter(Tweet.search_id == search_id).all()
    
    @staticmethod
    def get_search_with_tweets(db: Session, search_id: int) -> Optional[Dict]:
        """Get search with all its tweets"""
        search = db.query(Search).filter(Search.id == search_id).first()
        if not search:
            return None
        
        tweets = db.query(Tweet).filter(Tweet.search_id == search_id).all()
        
        return {
            'search': search.to_dict(),
            'tweets': [tweet.to_dict() for tweet in tweets]
        }
