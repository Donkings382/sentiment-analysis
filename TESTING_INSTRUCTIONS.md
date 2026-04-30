# Frontend-Backend Integration - Testing Instructions

## What Was Updated:

### Backend (Already Running):
- ✅ Database: `searches` + `tweets` tables
- ✅ API Server: `http://localhost:8000`
- ✅ Endpoint: `POST /api/search`

### Frontend (Just Updated):
- ✅ SearchBar: Added date filters (start_date, end_date)
- ✅ API Service: Calls real backend instead of mock data
- ✅ SentimentSummary: Uses backend's explanation text

## How to Test:

### Step 1: Make Sure Backend is Running
```bash
cd c:\src\scrapeX\backend
python api_server.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Start Frontend
Open NEW terminal:
```bash
cd c:\src\scrapeX\sentiment-analysis
npm run dev
```

You should see:
```
Local: http://localhost:5173/
```

### Step 3: Test the App

1. **Open browser**: Go to `http://localhost:5173`

2. **Search without dates**:
   - Type: `wizkid`
   - Leave date fields empty
   - Click "Search"
   - Should show 4 tweets with sentiment analysis

3. **Search with dates**:
   - Type: `wizkid`
   - Start Date: `2024-01-01`
   - End Date: `2024-02-28`
   - Click "Search"
   - Should show only tweets from Jan-Feb 2024

4. **Check the explanation**:
   - Scroll down to sentiment summary
   - You should see the detailed explanation from backend (not hardcoded text)
   - It will mention specific tweets, engagement numbers, etc.

## What to Look For:

✅ **Date pickers appear** in search form
✅ **Loading spinner** shows while scraping
✅ **Real tweets** from backend (not random mock data)
✅ **Sentiment scores** match backend analysis
✅ **Explanation text** is detailed and mentions specific tweets
✅ **Each search creates new database entry** (check pgAdmin)

## Troubleshooting:

**Problem**: "Failed to fetch tweets"
- **Solution**: Make sure backend is running on port 8000

**Problem**: CORS error in browser console
- **Solution**: Backend already has CORS enabled for localhost:5173

**Problem**: No tweets found
- **Solution**: Try queries in mock data: wizkid, fuel price, bitcoin, davido, python programming

## Available Mock Queries:
- wizkid
- fuel price
- bitcoin
- davido
- python programming

(Remember: API_MODE=development in .env uses mock data)
