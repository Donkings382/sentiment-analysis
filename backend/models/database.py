from sqlalchemy import Column, String, Integer, DateTime, Text, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv() 
Base = declarative_base()

class Search(Base):
    """Searches table - stores each scrape event"""
    __tablename__ = 'searches'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(String(500), nullable=False)
    start_date = Column(String(100), nullable=True)
    end_date = Column(String(100), nullable=True)
    total_tweets = Column(Integer, default=0)
    positive_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    average_sentiment = Column(Float, nullable=True)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tweets = relationship("Tweet", back_populates="search", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'query': self.query,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'total_tweets': self.total_tweets,
            'positive_count': self.positive_count,
            'neutral_count': self.neutral_count,
            'negative_count': self.negative_count,
            'average_sentiment': self.average_sentiment,
            'explanation': self.explanation,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Tweet(Base):
    """Tweets table - stores individual tweets"""
    __tablename__ = 'tweets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    search_id = Column(Integer, ForeignKey('searches.id'), nullable=False)
    tweet_id = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(String(100), nullable=True)
    likes = Column(Integer, default=0)
    replies = Column(Integer, default=0)
    retweets = Column(Integer, default=0)
    url = Column(String(1000), nullable=True)
    vader_score = Column(Float, nullable=True)
    textblob_score = Column(Float, nullable=True)
    combined_score = Column(Float, nullable=True)
    sentiment_label = Column(String(20), nullable=True)
    
    search = relationship("Search", back_populates="tweets")
    
    def to_dict(self):
        return {
            'id': self.id,
            'search_id': self.search_id,
            'tweet_id': self.tweet_id,
            'text': self.text,
            'date': self.date,
            'likes': self.likes,
            'replies': self.replies,
            'retweets': self.retweets,
            'url': self.url,
            'vader_score': self.vader_score,
            'textblob_score': self.textblob_score,
            'combined_score': self.combined_score,
            'sentiment_label': self.sentiment_label
        }


# Database connection setup
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/scraper_db')

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
