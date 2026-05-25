# Frontend-Backend Integration Test Plan

## Setup

1. **Backend Server** (Terminal: python)
   - Ensure Django server is running: `python manage.py runserver`
   - Should be accessible at: `http://localhost:8000`

2. **Frontend Server** (Terminal: node)
   - Restart the dev server to pick up .env changes: `npm start`
   - Should be accessible at: `http://localhost:3000`

## Integration Points Fixed

### 1. API Response Handling ✅
- **Problem**: DRF returns paginated responses with structure: `{ count, next, previous, results: [...] }`
- **Solution**: Updated `client.js` to extract `results` array and return as `data`
- **Impact**: Pages now receive arrays they can `.map()` over

### 2. Environment Configuration ✅
- **Backend (.env)**: CORS configured for `http://localhost:3000`
- **Frontend (.env)**: API URL points to `http://localhost:8000/api`

### 3. Models Fixed ✅
- Removed PostgreSQL-only `ArrayField` imports
- Converted all `ArrayField` → `JSONField` for SQLite compatibility
- Migrations created successfully

## Test Endpoints

### Trends Page (`http://localhost:3000/trends`)
- ✅ Should load without "trends.map is not a function" error
- Empty state should show: "No trends found. Check back soon!"
- No API errors in console

### Competitors Page (`http://localhost:3000/competitors`)
- ✅ Should load competitor data
- Empty state: "No competitors data available"

### Sentiment Page (`http://localhost:3000/sentiment`)
- ✅ Should load sentiment data
- Empty state: "No sentiment data available"

### AI Agent Page (`http://localhost:3000/ai-agent`)
- ✅ Form should allow input
- Strategy generation should work (or show proper error)

## Debugging

If you still see errors:

1. **Check API Response**: Open DevTools → Network tab
   - Go to `http://localhost:3000/trends`
   - Look for `GET http://localhost:8000/api/trends/`
   - Inspect response in Network tab
   - Should see: `{ "count": 0, "next": null, "previous": null, "results": [] }`

2. **Check Frontend Console**: 
   - Open DevTools → Console
   - Look for errors about API calls
   - Verify `response.data` is an array

3. **Check Backend Logs**:
   - Terminal showing Django should have request logs
   - Should see: `GET /api/trends/ HTTP/1.1" 200`

## Next Steps

1. Rebuild frontend: Close npm server and run `npm start` again
2. Navigate to each page and verify no ".map is not a function" errors
3. Use browser DevTools to inspect API responses
4. Populate sample data if needed
