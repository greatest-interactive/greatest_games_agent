# Data Collection Guide

## Quick Start

You have multiple ways to collect game market data:

### Option 1: Batch Script (Windows - Easiest)
1. Navigate to the project root directory
2. Double-click `collect_data.bat`
3. Wait for collection to complete
4. Results appear in your dashboard

### Option 2: PowerShell Script (Windows)
1. Open PowerShell
2. Navigate to project root: `cd path\to\project`
3. Run: `.\collect_data.ps1`
4. Or enable script execution first: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Option 3: Python Script
1. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
2. Run the collection script:
   ```
   python collect_data.py
   ```

### Option 4: Django Management Command
1. Navigate to backend directory:
   ```
   cd backend
   ```
2. Activate virtual environment:
   ```
   ..\venv\Scripts\activate
   ```
3. Run the command:
   ```
   python manage.py collect_trends --all
   ```

## What Gets Collected?

The scripts collect trending games from:
- **Steam** - Top trending indie and new releases
- **Itch.io** - Independent game marketplace
- **Epic Games Store** - AAA and featured titles

Each game includes:
- Title and developer
- Rating and review count
- Platform and price
- Genres and tags
- Trending score (0-100)
- Engagement metrics

## Data Sources

The collection uses **Bright Data APIs** to scrape real marketplace data:
- Web Scraper API for marketplace listings
- SERP API for search trends
- Rotated IP addresses to avoid blocking

## Viewing Results

1. Start the development servers:
   ```
   # Terminal 1 - Backend
   cd backend
   python manage.py runserver
   
   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

2. Visit the dashboard at `http://localhost:3000`

3. Navigate to:
   - **Dashboard** - View trending stats and top games
   - **Competitors** - Browse all scraped games
   - **Trends** - Explore market trends
   - **Sentiment** - Analyze player feedback

## Troubleshooting

### Error: "Connection aborted" or "HTTPSConnectionPool read timeout"
- Your ISP may be blocking HTTPS connections to Bright Data
- **Solution**: Use Windscribe VPN or similar (free option available)
- Once connected, run the collection script again

### Error: "BRIGHT_DATA_API_KEY not found"
- Check your `.env` file has the API key
- Make sure it's in `backend/.env`
- Example: `BRIGHT_DATA_API_KEY=a799b10b-51db-4a62-a307-642d48f2ac17`

### Error: "Database is locked"
- Another process may be using the database
- Kill the Python process and try again
- Or restart both backend servers

### No data appearing in dashboard
- Wait a few seconds after collection completes
- Refresh the browser with Ctrl+F5 (hard refresh)
- Check browser console (F12) for errors
- Verify backend is running on port 8000

## Scheduling Automatic Collection

To automatically collect data on a schedule:

### Windows Task Scheduler
1. Open Task Scheduler
2. Create new task: "Collect Game Data"
3. Trigger: Daily at 8 AM (or your preferred time)
4. Action: `C:\path\to\project\collect_data.bat`
5. Configure to run even if user is not logged in

### Linux/Mac (Cron)
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 8 AM
0 8 * * * cd /path/to/project && /path/to/venv/bin/python collect_data.py
```

## API Rate Limits

Bright Data allows:
- **10 concurrent requests**
- **Automatic retry** on failure
- **30-60 second timeout** per request

The collection script respects these limits and handles errors gracefully.

## Next Steps

Once you have data collected:
1. ✅ Data Collection (You are here)
2. ⏳ Phase 2: AI Insights (OpenAI integration)
3. ⏳ Phase 3: Launch Strategy Generation

For Phase 2, the OpenAI integration will analyze this data to generate:
- Market insights and opportunities
- Competitor analysis reports
- Launch strategy recommendations
- Sentiment analysis breakdowns
