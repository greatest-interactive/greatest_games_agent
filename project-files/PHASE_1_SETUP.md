# Phase 1 Setup: Bright Data Integration

## What We've Created

✅ **Bright Data Service Module** (`api/services/bright_data.py`)
- BrightDataClient class for API interactions
- Methods for SERP searches, marketplace scraping
- Mock data fallback for testing

✅ **Database Models**
- `ScrapingJob` - Track Bright Data collection jobs
- `ScrapedGame` - Store game data from scrapes

✅ **Management Command**
- `collect_trends` - Collect gaming trends via Bright Data
- Supports: Steam, itch.io, Epic Games Store
- Includes mock data for testing

✅ **API Endpoints**
- `/api/scraping-jobs/` - List/view scraping jobs
- `/api/scraped-games/` - View scraped games
- `/api/scraped-games/trending/` - Get trending games
- `/api/scraped-games/by_platform/` - Games grouped by platform
- `/api/scraping-jobs/{id}/results/` - Get games from a job

## Quick Start (3 Steps)

### Step 1: Create Database Migrations
Run these commands in the `backend/` directory:

```powershell
cd backend
python manage.py makemigrations
python manage.py migrate
```

You should see:
```
Migrations for 'api':
  - Create model ScrapingJob
  - Create model ScrapedGame
```

### Step 2: Collect Trending Data
Run the management command to collect games from Steam, itch.io, and Epic:

```powershell
python manage.py collect_trends --all
```

Output should show:
```
Starting trend collection...
Collecting from steam...
  - Searched: best horror games 2026
  - Searched: top indie games steam
  - Created trend: Hollow Knight: Silksong
  ✓ Collected 3 games from steam
Collecting from itch_io...
  ✓ Collected 2 games from itch_io
Collecting from epic...
  ✓ Collected 1 games from epic
Trend collection completed!
```

### Step 3: Verify API Endpoints

Open browser and test:

**Check scraping jobs:**
```
http://localhost:8000/api/scraping-jobs/
```
Should return list of jobs with status 'completed'

**Check scraped games:**
```
http://localhost:8000/api/scraped-games/
```
Should return games from all platforms

**Check trending games:**
```
http://localhost:8000/api/scraped-games/trending/
```
Should return games with high trending_score

## Real Bright Data Integration

When you're ready to use REAL Bright Data APIs:

### 1. Test Your API Key
```powershell
python manage.py shell
```

```python
from api.services.bright_data import bright_data_client

# Test SERP search
result = bright_data_client.search_serp("best horror games 2026")
print(result)
```

If successful, you'll see actual search results.

### 2. Handle Responses
The real Bright Data returns results like:
```json
{
  "results": [
    {
      "url": "...",
      "title": "...",
      "snippets": "...",
      "rating": 4.8
    }
  ]
}
```

Parser logic in `bright_data.py` extracts this into game objects.

### 3. Scale Collection
Once working, schedule jobs:
- Daily: `collect_trends --all`
- Hourly: `collect_trends --source steam`

## File Structure Created

```
backend/
├── api/
│   ├── services/
│   │   ├── __init__.py
│   │   └── bright_data.py          ← Bright Data client
│   ├── management/
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── collect_trends.py   ← Data collection command
│   ├── models.py                    ← Added ScrapingJob, ScrapedGame
│   ├── serializers.py               ← Added serializers
│   ├── views.py                     ← Added ViewSets
│   └── urls.py                      ← Updated routing
└── .env                             ← Updated with API key
```

## Next Steps (After Testing)

1. **Phase 2: AI Analysis**
   - Set up OpenAI integration
   - Generate insights from scraped data
   - Create analysis views

2. **Phase 3: Dashboard Charts**
   - Install Recharts in frontend: `npm install recharts`
   - Create visualization components
   - Connect to scraped data endpoints

3. **Frontend Display**
   - Update Competitors page to show `ScrapedGame` data
   - Add trending games section
   - Create platform filter

## Troubleshooting

**Error: "No such table: api_scrapingjob"**
- Run: `python manage.py migrate`

**Error: "bright_data_client import failed"**
- Check .env has `BRIGHT_DATA_API_KEY` set
- Run: `python manage.py shell` to test import

**No results from search_serp()**
- Bright Data API might rate-limit free tier
- Check mock data fallback is working
- Use: `python manage.py collect_trends --all` to test

## Demo Data Available

After `python manage.py collect_trends --all`, you'll have:
- 6+ games across Steam, itch.io, Epic
- Trending scores calculated
- Mock engagement metrics
- All accessible via `/api/scraped-games/`

Ready for frontend display! 🚀
