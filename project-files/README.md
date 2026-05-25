# Greatest Game Agent
## AI-Powered Game Market Intelligence Platform

An intelligent platform that uses AI agents and live web data to help indie game studios, solo developers, and publishers discover trends, track competitors, analyze player sentiment, and generate data-driven launch strategies.

### 🎮 Quick Links
- [Vision](#vision)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Contributing](#contributing)

---

## 🎯 Vision

Greatest Game Agent addresses a critical problem: **indie developers build games blindly**. 

Unlike large publishers with teams of analysts, indie studios lack:
- Real-time market intelligence
- Trend forecasting tools
- Competitor monitoring systems
- Structured player feedback analysis
- Affordable business research tools

**Our Solution**: AI agents powered by live web data, enabling indie game creators to make data-driven decisions from day one.

---

## ✨ Core Features

### 1. **Trend Discovery Agent**
- Search live web data for emerging game niches
- Identify trending mechanics, genres, and aesthetics
- Detect market gaps and opportunities
- Analyze monetization trends

### 2. **Competitor Intelligence Dashboard**
- Track Steam releases in real-time
- Monitor pricing changes and review spikes
- Analyze player tags and social discussions
- Monitor influencer coverage

### 3. **AI Launch Strategy Generator**
- Generate data-driven launch recommendations
- Suggest optimal pricing strategies
- Identify best release timing
- Create viral marketing suggestions
- Analyze competitive landscape

### 4. **Live Gaming Sentiment Analysis**
- Scrape Reddit, YouTube, TikTok, Steam reviews
- Identify sentiment trends
- Extract pain points and feature requests
- Track gameplay preferences

---

## 🛠 Tech Stack

### Frontend
- **React 18** - UI framework
- **React Router** - Navigation
- **Recharts** - Data visualization
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API
- **PostgreSQL** - Database
- **Celery** - Task queue
- **Redis** - Caching

### AI & Data
- **OpenAI GPT-4** - Strategic analysis
- **Bright Data** - Web intelligence
  - SERP API - Search trends
  - Web Scraper API - Structured data
  - Scraping Browser - Dynamic content

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis (optional, for task queue)

### Backend Setup

```bash
# Navigate to backend
cd project-files/backend

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys and database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
# Navigate to frontend
cd project-files/frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env

# Start development server
npm start
```

The app will open at `http://localhost:3000`

---

## 📊 System Architecture

```
User Query 
    ↓
AI Agent Controller
    ↓
Bright Data APIs (SERP, Web Scraper, Browser)
    ↓
Web Data Collection
    ↓
Data Structuring & Validation
    ↓
AI Analysis Engine (OpenAI)
    ↓
Database Storage
    ↓
Dashboard + API Responses
```

---

## 📁 Project Structure

```
greatest-game-agent/
├── backend/
│   ├── greatest_game_agent/       # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── api/                       # API app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── scraper/                   # Bright Data integration
│   │   └── bright_data_integration.py
│   ├── ai_analysis/               # OpenAI analysis engine
│   │   └── analysis_engine.py
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Navigation.js
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   │   ├── Trends.js
│   │   │   ├── Competitors.js
│   │   │   ├── Sentiment.js
│   │   │   ├── Reports.js
│   │   │   └── AIAgent.js
│   │   ├── api/
│   │   │   └── client.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
├── docs/
│   ├── API.md
│   ├── DEVELOPMENT.md
│   └── DEPLOYMENT.md
└── README.md
```

---

## 🔌 API Endpoints

### Games
- `GET /api/games/` - List all games
- `GET /api/games/{id}/` - Get game details
- `POST /api/games/` - Create new game entry

### Competitors
- `GET /api/competitors/` - List competitors
- `GET /api/competitors/trending/` - Get trending competitors
- `GET /api/competitors/{id}/` - Get competitor details

### Trends
- `GET /api/trends/` - List all trends
- `GET /api/trends/{id}/` - Get trend details
- `GET /api/trends/?category=genre` - Filter by category

### Market Analysis
- `GET /api/analysis/` - List analyses
- `POST /api/analysis/` - Create analysis

### Player Sentiment
- `GET /api/sentiment/` - List sentiment data
- `GET /api/sentiment/?source=reddit` - Filter by source

### Launch Strategies
- `GET /api/strategies/` - List strategies
- `POST /api/strategies/generate/` - Generate new strategy

---

## 🌟 Key Components

### AI Analysis Engine
Powered by GPT-4, analyzes market data and generates insights:
- Market trend analysis
- Sentiment summaries
- Launch strategy recommendations
- Competitive positioning

### Bright Data Integration
Collects live web data:
- SERP API: Search trends and game rankings
- Web Scraper: Structured data from Steam, itch.io, etc.
- Scraping Browser: JavaScript-rendered content

### Database Models
- **Game**: Marketplace games and metadata
- **Competitor**: Tracked competitor metrics
- **Trend**: Emerging trends and opportunities
- **MarketAnalysis**: AI-generated insights
- **PlayerSentiment**: Social sentiment data
- **LaunchStrategy**: Strategic recommendations

---

## 📈 Data Flow

1. **Data Collection**: Bright Data APIs scrape web sources
2. **Storage**: Raw data stored in PostgreSQL
3. **Analysis**: OpenAI analyzes data patterns
4. **Insights**: AI generates strategic recommendations
5. **Visualization**: Dashboard displays results in real-time

---

## 🎓 Development Guide

### Adding a New Feature

1. **Backend**: Add model in `api/models.py`
2. **Serializers**: Create serializer in `api/serializers.py`
3. **Views**: Add viewset in `api/views.py`
4. **URLs**: Register in `api/urls.py`
5. **Frontend**: Create React component in `src/pages/`
6. **API**: Add client function in `src/api/client.js`

### Running Tests

```bash
cd backend
python manage.py test api
```

### Code Style

```bash
# Format code
black .

# Lint
flake8 .
```

---

## 🚢 Deployment

### Backend (Heroku Example)
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

### Frontend (Vercel Example)
```bash
npm run build
vercel --prod
```

---

## 📝 Environment Variables

### Backend (.env)
```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

DB_NAME=greatest_game_agent
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

BRIGHT_DATA_API_KEY=your-bright-data-key
OPENAI_API_KEY=your-openai-key

CELERY_BROKER_URL=redis://localhost:6379/0
```

### Frontend (.env)
```
REACT_APP_API_URL=https://api.yourdomain.com/api
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙋 Support

For questions or support, please open an issue on GitHub.

---

## 🎮 The Story

Built by Greatest Interactive to support our own game development process. We realized indie studios face a massive information gap. While AAA publishers have teams of market analysts, solo developers guess. Greatest Game Agent democratizes market intelligence for game creators.

**"AI agents should not just chat. They should research, analyze, and make strategic business decisions using live web data."**
