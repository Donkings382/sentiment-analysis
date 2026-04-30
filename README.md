# Twitter Scraper - Phase 6: Sentiment Analysis

A production-grade Twitter scraper with PostgreSQL database storage and VADER + TextBlob sentiment analysis.

## 🚀 Current Features (Phase 6)

✅ **Official Twitter API v2** - Uses Bearer Token authentication  
✅ **Playwright Stealth Mode** - Enhanced anti-bot detection bypass  
✅ **Human-like Behavior** - Random delays, mouse movements, gradual scrolling  
✅ **PostgreSQL Database** - Persistent storage with full CRUD operations  
✅ **FastAPI Backend** - RESTful API with background task processing  
✅ **Sentiment Analysis** - VADER + TextBlob combined approach  
✅ **Analysis Tracking** - Separate analysis status and JSON export  
✅ **Job Management** - Search, filter, and track all scraping jobs

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Setup PostgreSQL Database
See [SETUP_PHASE4.md](SETUP_PHASE4.md) for detailed PostgreSQL setup instructions.

### 3. Configure Environment
Create a `.env` file:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/scraper_db
```

### 4. Start API Server
```bash
python api_server.py
```

API will be available at:
- Server: http://localhost:8000
- Docs: http://localhost:8000/docs

## 📊 Phase 6: Sentiment Analysis

### Workflow:
1. **Scrape** → POST `/scrape` → Saves to PostgreSQL + JSON
2. **Analyze** → POST `/analyze/{job_id}` → Runs sentiment analysis
3. **Results** → GET `/sentiment/{job_id}` → Get sentiment statistics

### Example Usage:

#### 1. Start Scraping Job
```bash
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Wizkid",
    "max_results": 20,
    "scraper_type": "twitter"
  }'
```

#### 2. Check Status
```bash
curl http://localhost:8000/status/{job_id}
```

#### 3. Analyze Sentiment
```bash
curl -X POST http://localhost:8000/analyze/{job_id}
```

#### 4. Get Sentiment Results
```bash
curl http://localhost:8000/sentiment/{job_id}
```

### Sentiment Scoring:
- **VADER Score** - Social media optimized (-1 to +1)
- **TextBlob Score** - General text sentiment (-1 to +1)
- **Combined Score** - Average of both scores
- **Label** - Positive (≥0.15), Negative (≤-0.15), Neutral (between)

### Output Files:
- **Raw Data**: `{query}_{job_id}_{timestamp}.json`
- **Analyzed Data**: `{query}_{job_id}_analyzed_{timestamp}.json`

See [PHASE6_SENTIMENT.md](PHASE6_SENTIMENT.md) for complete documentation.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| POST | `/scrape` | Start scraping job |
| GET | `/status/{job_id}` | Get job status and results |
| GET | `/jobs` | List all jobs |
| GET | `/search` | Search jobs by query/status |
| GET | `/statistics` | Get overall statistics |
| POST | `/analyze/{job_id}` | Analyze sentiment for job |
| GET | `/sentiment/{job_id}` | Get sentiment statistics |
| GET | `/health` | Health check |

## 🧪 Testing

### Test Full Workflow:
```bash
python test_phase6.py
```

This will:
1. Create a scraping job
2. Wait for completion
3. Trigger sentiment analysis
4. Display results with sentiment scores

### Manual Testing:
```bash
# Test scraper directly
python test_scraper.py

# Test sentiment on existing data
python scrape_x.py
```

## 📁 Project Structure

```
scrapeX/
├── api_server.py              # FastAPI server (Phase 6)
├── scraper_engine.py          # Core scraping logic with stealth
├── sentiment_analyzer.py      # VADER + TextBlob sentiment analysis
├── database.py                # SQLAlchemy models (Jobs, Results)
├── db_service.py              # Database service layer
├── test_scraper.py            # Direct scraper testing
├── test_phase6.py             # Phase 6 workflow testing
├── scrape_x.py                # Standalone sentiment analysis
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration
├── PHASE6_SENTIMENT.md        # Phase 6 documentation
└── SETUP_PHASE4.md            # PostgreSQL setup guide
```

## 🗄️ Database Schema

### Jobs Table
- `job_id` (PK) - Unique job identifier
- `query` - Search query
- `scraper_type` - 'twitter' or 'generic'
- `status` - queued, processing, completed, failed
- `analysis_status` - pending, processing, completed, failed
- `results_count` - Number of results scraped
- `filename` - Raw data JSON filename
- `analysis_filename` - Analyzed data JSON filename
- Timestamps: created_at, started_at, completed_at, analyzed_at

### Results Table
- `result_id` (PK) - Auto-increment ID
- `job_id` (FK) - Links to Jobs table
- `text` - Tweet content
- `date`, `likes`, `replies`, `retweets`, `url`
- `vader_score` - VADER sentiment score
- `textblob_score` - TextBlob sentiment score
- `combined_score` - Average sentiment score
- `sentiment_label` - Positive, Neutral, Negative

## 🎯 Development Phases

- ✅ **Phase 1**: Foundation (Scraper Engine)
- ✅ **Phase 2**: Background Processing (FastAPI + Async)
- ✅ **Phase 3**: Enhanced Stealth (playwright-stealth)
- ✅ **Phase 4**: PostgreSQL Database
- ⏭️ **Phase 5**: Proxy Rotation (SKIPPED for MVP)
- ✅ **Phase 6**: Sentiment Analysis (CURRENT)

## 💡 Key Design Decisions

1. **Database-First Approach** - PostgreSQL is single source of truth
2. **Separate Analysis** - Analyze after scraping (not during)
3. **Background Processing** - Non-blocking async tasks
4. **Stealth Mode** - Human-like behavior + playwright-stealth
5. **No Proxies (MVP)** - Cost-effective with delays + stealth

## 🔧 Requirements

- Python 3.8+
- PostgreSQL 12+
- Chromium (installed via Playwright)

## 📚 Documentation

- [PHASE6_SENTIMENT.md](PHASE6_SENTIMENT.md) - Sentiment analysis guide
- [SETUP_PHASE4.md](SETUP_PHASE4.md) - PostgreSQL setup
- API Docs: http://localhost:8000/docs (when server running)

## 🐛 Troubleshooting

See [PHASE6_SENTIMENT.md](PHASE6_SENTIMENT.md) for common issues and solutions.

## 📝 License

Built from scratch per project requirements - no paid services used.
