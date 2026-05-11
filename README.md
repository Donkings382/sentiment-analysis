# Twitter Sentiment Analysis Platform

**Live Demo:** [https://sentiment-analysis-peach.vercel.app](https://sentiment-analysis-peach.vercel.app)

A full-stack web application that analyzes Twitter sentiment in real-time using natural language processing (NLP). Search any topic and instantly understand public opinion through AI-powered sentiment analysis.

## 🎯 Real-World Use Case

**Scenario:** A marketing manager at a beverage company wants to understand public reaction to their new product launch.

**Problem:** Manually reading thousands of tweets is impossible. They need instant insights into whether the sentiment is positive, negative, or neutral.

**Solution:** 
1. Enter search query: "new energy drink launch"
2. Get instant analysis of tweets with sentiment scores
3. View summary: 65% positive, 20% neutral, 15% negative
4. Identify trending concerns or praise points
5. Make data-driven decisions for marketing strategy

**Other Use Cases:**
- **Brand Monitoring:** Track brand reputation and customer satisfaction
- **Crisis Management:** Detect negative sentiment spikes early
- **Product Feedback:** Analyze customer reactions to new features
- **Competitor Analysis:** Compare sentiment across competing products
- **Political Campaigns:** Gauge public opinion on policies
- **Event Monitoring:** Track real-time reactions during live events

## 🚀 Features

- **Real-time Search:** Query Twitter data by keyword with date filters
- **AI Sentiment Analysis:** Dual-engine analysis (VADER + TextBlob) for accuracy
- **Visual Dashboard:** Clean UI showing sentiment distribution and confidence scores
- **Tweet Metrics:** View likes, retweets, and replies for each tweet
- **Summary Reports:** Get overall sentiment with detailed explanations
- **PostgreSQL Storage:** All searches and results saved for historical analysis

## 🛠️ Tech Stack

**Frontend:**
- React 18 + Vite
- CSS Modules
- Responsive Design

**Backend:**
- FastAPI (Python)
- Twitter API v2
- NLTK (VADER Sentiment)
- TextBlob (Polarity Analysis)

**Database:**
- PostgreSQL (Aiven Managed)

**Deployment:**
- Vercel (Frontend + Backend)

## 📦 Project Structure

```
scrapeX/
├── backend/
│   ├── api_server.py          # FastAPI REST API
│   ├── scrapers/              # Twitter data fetching
│   ├── analyzers/             # Sentiment analysis engine
│   ├── models/                # Database models
│   └── services/              # Business logic
├── sentiment-analysis/        # React frontend
│   └── src/
│       ├── components/        # UI components
│       └── services/          # API integration
├── data/
│   ├── mock_api_data.json     # Development mock data
│   └── exports/               # JSON exports
└── vercel.json                # Deployment config
```

## 🏃 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL database

### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Configure environment
cp ../.env.example ../.env
# Edit .env with your credentials

# Initialize database
python -c "from models.database import init_db; init_db()"

# Run server
python api_server.py
```

### Frontend Setup

```bash
cd sentiment-analysis
npm install
npm run dev
```

Visit `http://localhost:5173`

## 🔧 Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# API Mode (development uses mock data)
API_MODE=development

# Twitter API (production only)
TWITTER_BEARER_TOKEN=your_token_here
```

### Development Mode
Uses mock data from `data/mock_api_data.json` - no Twitter API required.

Available mock queries: `fuel price`, `wizkid`, `climate change`

### Production Mode
Set `API_MODE=production` and provide valid `TWITTER_BEARER_TOKEN`.

## 📊 API Endpoints

### POST `/api/search`
Search and analyze tweets

**Request:**
```json
{
  "query": "climate change",
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-01-31T23:59:59Z",
  "max_results": 100
}
```

**Response:**
```json
{
  "query": "climate change",
  "total": 100,
  "tweets": [...],
  "summary": {
    "overall_sentiment": "Neutral",
    "positive": 45,
    "negative": 30,
    "neutral": 25,
    "average_score": 0.12,
    "confidence": "Medium",
    "explanation": "..."
  }
}
```

## 🎨 Sentiment Analysis

**Dual-Engine Approach:**
1. **VADER:** Optimized for social media text (emojis, slang, capitalization)
2. **TextBlob:** General-purpose polarity analysis

**Combined Score:** Weighted average for balanced results

**Classification:**
- Positive: score > 0.05
- Negative: score < -0.05
- Neutral: -0.05 ≤ score ≤ 0.05

## 🚀 Deployment

Deployed on Vercel with:
- Serverless FastAPI backend
- Static React frontend
- Managed PostgreSQL (Aiven)

```bash
vercel
```

## 📝 License

MIT

## 👤 Author

Built with ❤️ for real-time social media insights

---

**Live App:** [https://sentiment-analysis-peach.vercel.app](https://sentiment-analysis-peach.vercel.app)
