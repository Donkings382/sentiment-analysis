# Twitter Sentiment Scraper UI

A minimalistic React-based user interface for searching and analyzing Twitter sentiment. Built with a clean white/grey color scheme and designed for easy backend integration.

## Features

- **Search Interface**: Clean search bar with enter key support
- **Loading States**: Visual feedback during API calls
- **Sentiment Analysis Display**: Shows positive/negative/neutral sentiment with confidence scores
- **Tweet Cards**: Displays tweet information including author, metrics, and sentiment
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: User-friendly error messages with retry functionality

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **CSS Modules** - Scoped styling
- **Inter Font** - Clean, modern typography

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Configuration

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:3000/api
```

## Project Structure

```
src/
├── components/
│   ├── Header.jsx          # App header with logo
│   ├── SearchBar.jsx       # Search input and button
│   ├── TweetList.jsx       # Container for tweet results
│   ├── TweetCard.jsx       # Individual tweet display
│   ├── SentimentSummary.jsx # Sentiment analysis overview
│   ├── LoadingSpinner.jsx  # Loading indicator
│   ├── ErrorMessage.jsx    # Error display
│   └── EmptyState.jsx      # Empty state display
├── services/
│   └── api.js              # API service layer
├── App.jsx                 # Main application component
├── App.module.css          # App styles
├── main.jsx               # Entry point
└── index.css              # Global styles
```

## Backend Integration

### API Service Configuration

The API service is located at `src/services/api.js`. Backend developers should:

1. Update the `API_BASE_URL` constant or set the `VITE_API_URL` environment variable
2. Replace the mock implementation in `searchTweets()` with actual API calls

### Expected API Response Format

The search endpoint should return an array of tweet objects with this structure:

```typescript
{
  id: string;           // Unique tweet identifier
  text: string;         // Tweet content
  author: {
    name: string;       // Author's display name
    username: string;   // Author's handle (@username)
    avatar: string;     // Profile image URL
  };
  createdAt: string;    // ISO date string
  metrics: {
    likes: number;
    retweets: number;
    replies: number;
  };
  sentiment: {          // NLP sentiment analysis result
    score: number;      // -1 to 1 (negative to positive)
    label: 'positive' | 'negative' | 'neutral';
    confidence: number; // 0 to 1
  };
}
```

### Example API Implementation

```javascript
// In src/services/api.js
export async function searchTweets(query) {
  const response = await fetch(
    `${API_BASE_URL}/tweets/search?q=${encodeURIComponent(query)}`
  );
  
  if (!response.ok) {
    throw new Error('Failed to fetch tweets');
  }
  
  return response.json();
}
```

## Design System

### Color Palette

- **Primary Background**: #fafafa (off-white)
- **Secondary Background**: #ffffff (pure white)
- **Primary Text**: #1f2937 (dark grey)
- **Secondary Text**: #6b7280 (medium grey)
- **Borders**: #e5e7eb (light grey)
- **Accent Button**: #374151 (charcoal)
- **Positive Sentiment**: #059669 (green)
- **Negative Sentiment**: #dc2626 (red)
- **Neutral Sentiment**: #6b7280 (grey)

### Typography

- **Font Family**: Inter, system fonts fallback
- **Font Weights**: 300 (light), 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |

## Development Notes

- The app uses CSS Modules for scoped styling
- All components are functional components with hooks
- The UI is fully responsive with mobile-first approach
- Mock data is used until backend integration is complete

## License

MIT