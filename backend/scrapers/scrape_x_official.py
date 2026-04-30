import requests
import json
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.database import SessionLocal, init_db
from services.db_service import DatabaseService
from analyzers.sentiment_analyzer import SentimentAnalyzer

load_dotenv()

# Configuration
API_MODE = os.getenv("API_MODE", "development")
MOCK_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'mock_api_data.json')
TWITTER_API_URL = os.getenv("TWITTER_API_URL", "https://api.x.com")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
EXPORTS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'exports')


def parse_date_input(date_str):
    """Convert user-friendly date input to ISO 8601 format"""
    if not date_str:
        return None
    
    date_str = date_str.strip().lower()
    now = datetime.utcnow()
    
    # Handle relative dates
    if date_str == "today":
        target_date = now
    elif date_str == "yesterday":
        target_date = now - timedelta(days=1)
    elif date_str == "last week":
        target_date = now - timedelta(weeks=1)
    elif date_str == "last month":
        target_date = now - timedelta(days=30)
    elif date_str.startswith("last ") and date_str.endswith(" days"):
        try:
            days = int(date_str.split()[1])
            target_date = now - timedelta(days=days)
        except:
            print(f"WARNING: Invalid date format: {date_str}")
            return None
    else:
        try:
            if len(date_str) == 10:
                target_date = datetime.strptime(date_str, "%Y-%m-%d")
            elif len(date_str) == 16:
                target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            else:
                print(f"WARNING: Invalid date format: {date_str}")
                return None
        except ValueError:
            print(f"WARNING: Invalid date format: {date_str}")
            return None
    
    return target_date.strftime("%Y-%m-%dT%H:%M:%SZ")


def get_data_from_file(query, start_time=None, end_time=None, max_results=100):
    """Mock data source - reads from JSON file"""
    try:
        with open(MOCK_DATA_FILE, encoding='utf-8') as f:
            all_data = json.load(f)
    except FileNotFoundError:
        return {
            "data": [],
            "meta": {"result_count": 0},
            "error": f"Mock data file not found: {MOCK_DATA_FILE}"
        }
    
    query_lower = query.lower().strip()
    
    if query_lower not in all_data:
        available = ", ".join(all_data.keys())
        return {
            "data": [],
            "meta": {"result_count": 0},
            "error": f"No mock data for '{query}'. Available queries: {available}"
        }
    
    tweets = all_data[query_lower]
    
    # Filter by date range
    if start_time or end_time:
        filtered = []
        for tweet in tweets:
            tweet_date = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00"))
            
            if start_time:
                start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                if tweet_date < start:
                    continue
            
            if end_time:
                end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                if tweet_date > end:
                    continue
            
            filtered.append(tweet)
        tweets = filtered
    
    tweets = tweets[:max_results]
    
    return {
        "data": tweets,
        "meta": {
            "newest_id": tweets[0]["id"] if tweets else None,
            "oldest_id": tweets[-1]["id"] if tweets else None,
            "result_count": len(tweets)
        }
    }


def get_data_from_api(query, start_time=None, end_time=None, max_results=100):
    """Real Twitter API source"""
    url = f"{TWITTER_API_URL}/2/tweets/search/all"
    
    params = {
        "query": query,
        "max_results": max_results,
        "tweet.fields": "created_at,public_metrics,author_id,edit_history_tweet_ids"
    }
    
    if start_time:
        params["start_time"] = start_time
    if end_time:
        params["end_time"] = end_time
    
    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}",
        "User-Agent": "v2SearchPython"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {
                "data": [],
                "meta": {"result_count": 0},
                "error": "Authentication Error: Invalid Bearer Token"
            }
        elif response.status_code == 429:
            return {
                "data": [],
                "meta": {"result_count": 0},
                "error": "Rate Limit Exceeded. Wait 15 minutes and try again."
            }
        else:
            return {
                "data": [],
                "meta": {"result_count": 0},
                "error": f"API Error: {response.status_code} - {response.text}"
            }
    except Exception as e:
        return {
            "data": [],
            "meta": {"result_count": 0},
            "error": f"Connection Error: {e}"
        }


def fetch_tweets(query, start_time=None, end_time=None, max_results=100):
    """Universal function - automatically uses mock or real API"""
    if API_MODE == "development":
        print("Using MOCK data (development mode)\n")
        return get_data_from_file(query, start_time, end_time, max_results)
    else:
        print("Using REAL Twitter API (production mode)\n")
        return get_data_from_api(query, start_time, end_time, max_results)


def main():
    print("\n" + "="*60)
    print("TWITTER SCRAPER WITH SENTIMENT ANALYSIS")
    print("="*60)
    print(f"Mode: {API_MODE.upper()}")
    print("="*60 + "\n")
    
    init_db()
    db = SessionLocal()
    analyzer = SentimentAnalyzer()
    
    try:
        query = input("Enter search query: ").strip()
        if not query:
            print("ERROR: Query is required")
            return
        
        print("\nDate formats: 'today', 'yesterday', 'last week', '2024-01-15', or press Enter to skip")
        start_input = input("Start date [optional]: ").strip()
        end_input = input("End date [optional]: ").strip()
        
        start_time = parse_date_input(start_input) if start_input else None
        end_time = parse_date_input(end_input) if end_input else None
        
        if start_input and not start_time:
            print("ERROR: Invalid start date")
            return
        if end_input and not end_time:
            print("ERROR: Invalid end date")
            return
        
        if start_time:
            print(f"Start: {start_time}")
        if end_time:
            print(f"End: {end_time}")
        
        max_input = input("Max results [default: 100]: ").strip()
        max_results = int(max_input) if max_input else 100
        
        print(f"\nFetching tweets for '{query}'...")
        
        data = fetch_tweets(query, start_time, end_time, max_results)
        
        if "error" in data:
            print(f"\nERROR: {data['error']}")
            return
        
        if "data" in data and data["data"]:
            tweets = data["data"]
            
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
            
            print(f"\nAnalyzing sentiment for {len(clean_data)} tweets...")
            
            texts = [tweet['text'] for tweet in clean_data]
            sentiment_results = analyzer.analyze_batch(texts)
            
            for i, tweet in enumerate(clean_data):
                tweet.update(sentiment_results[i])
            
            summary = analyzer.generate_summary(clean_data)
            
            search = DatabaseService.create_search(
                db=db,
                query=query,
                start_date=start_time,
                end_date=end_time
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
            
            os.makedirs(EXPORTS_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(EXPORTS_DIR, f"{query.lower().replace(' ', '_')}_{timestamp}.json")
            
            export_data = {
                "query": query,
                "timestamp": timestamp,
                "summary": summary,
                "tweets": clean_data
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"\nSUCCESS! Scraped and analyzed {len(clean_data)} tweets")
            print(f"Saved to: {os.path.abspath(filename)}")
            print(f"Saved to database: Search ID {search.id} with {len(clean_data)} tweets")
            
            print("\n" + "="*60)
            print("SENTIMENT ANALYSIS SUMMARY")
            print("="*60)
            print(f"Overall Sentiment: {summary['overall_sentiment']}")
            print(f"Positive: {summary['positive']} ({summary['positive_percent']}%)")
            print(f"Neutral: {summary['neutral']} ({summary['neutral_percent']}%)")
            print(f"Negative: {summary['negative']} ({summary['negative_percent']}%)")
            print("\nExplanation:")
            try:
                print(summary['explanation'])
            except UnicodeEncodeError:
                print(summary['explanation'].encode('ascii', 'ignore').decode('ascii'))
            print("="*60)
            
            return {
                "tweets": clean_data,
                "summary": summary
            }
        else:
            print("\nNo tweets found")
            print("Try a different query or date range")
            return None
    
    finally:
        db.close()


if __name__ == "__main__":
    try:
        result = main()
        
        if result:
            print("\nScraping and sentiment analysis completed successfully!")
    except KeyboardInterrupt:
        print("\n\nCancelled by user\n")
    except Exception as e:
        print(f"\nError: {e}\n")
        import traceback
        traceback.print_exc()
