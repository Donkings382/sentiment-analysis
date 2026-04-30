from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from models.database import SessionLocal, init_db
from services.db_service import DatabaseService
from scrapers.scrape_x_official import fetch_tweets
from analyzers.sentiment_analyzer import SentimentAnalyzer

app = FastAPI(title="Twitter Sentiment Analysis API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

class SearchRequest(BaseModel):
    query: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    max_results: Optional[int] = 100

@app.get("/")
def root():
    return {
        "message": "Twitter Sentiment Analysis API",
        "version": "1.0",
        "endpoints": {
            "POST /api/search": "Search and analyze tweets",
            "GET /health": "Health check"
        }
    }

@app.post("/api/search")
def search_tweets(request: SearchRequest):
    """
    Scrape tweets NOW and return results immediately
    """
    db = SessionLocal()
    analyzer = SentimentAnalyzer()
    
    try:
        # Fetch tweets from API/mock
        data = fetch_tweets(
            query=request.query,
            start_time=request.start_date,
            end_time=request.end_date,
            max_results=request.max_results
        )
        
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        if not data.get("data"):
            return {
                "query": request.query,
                "total": 0,
                "tweets": [],
                "summary": {
                    "total": 0,
                    "positive": 0,
                    "negative": 0,
                    "neutral": 0,
                    "positive_percent": 0,
                    "negative_percent": 0,
                    "neutral_percent": 0,
                    "average_score": 0,
                    "overall_sentiment": "Neutral",
                    "confidence": "Low",
                    "explanation": "No tweets found for this query."
                }
            }
        
        tweets = data["data"]
        
        # Transform to clean format
        clean_data = []
        for tweet in tweets:
            clean_data.append({
                "id": tweet.get("id"),
                "date": tweet.get("created_at"),
                "text": tweet.get("text"),
                "likes": tweet.get("public_metrics", {}).get("like_count", 0),
                "replies": tweet.get("public_metrics", {}).get("reply_count", 0),
                "retweets": tweet.get("public_metrics", {}).get("retweet_count", 0),
                "url": f"https://twitter.com/i/web/status/{tweet.get('id')}"
            })
        
        # Analyze sentiment
        texts = [tweet['text'] for tweet in clean_data]
        sentiment_results = analyzer.analyze_batch(texts)
        
        for i, tweet in enumerate(clean_data):
            tweet.update(sentiment_results[i])
        
        # Generate summary
        summary = analyzer.generate_summary(clean_data)
        
        # Save to database
        search = DatabaseService.create_search(
            db=db,
            query=request.query,
            start_date=request.start_date,
            end_date=request.end_date
        )
        
        DatabaseService.create_tweets_bulk(
            db=db,
            search_id=search.id,
            tweets_data=clean_data
        )
        
        DatabaseService.update_search_summary(
            db=db,
            search_id=search.id,
            summary=summary
        )
        
        return {
            "query": request.query,
            "search_id": search.id,
            "total": len(clean_data),
            "tweets": clean_data,
            "summary": summary
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
