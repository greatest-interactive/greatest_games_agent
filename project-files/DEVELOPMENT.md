# Development Setup Guide

## Initial Setup

### 1. Database Setup

#### PostgreSQL Installation
- Download from https://www.postgresql.org/download/
- During installation, remember your password for the postgres user
- Create a new database:
  ```sql
  CREATE DATABASE greatest_game_agent;
  CREATE USER gga_user WITH PASSWORD 'your_password';
  ALTER ROLE gga_user SET client_encoding TO 'utf8';
  ALTER ROLE gga_user SET default_transaction_isolation TO 'read committed';
  ALTER ROLE gga_user SET default_transaction_deferrable TO on;
  ALTER ROLE gga_user SET timezone TO 'UTC';
  GRANT ALL PRIVILEGES ON DATABASE greatest_game_agent TO gga_user;
  ```

### 2. Backend Environment

```bash
cd project-files/backend

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Edit .env with:
# - Your database credentials
# - BRIGHT_DATA_API_KEY
# - OPENAI_API_KEY
```

### 3. Django Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Frontend Environment

```bash
cd project-files/frontend

npm install
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
```

## Running the Application

### Terminal 1 - Backend
```bash
cd project-files/backend
source venv/Scripts/activate
python manage.py runserver
```

### Terminal 2 - Frontend
```bash
cd project-files/frontend
npm start
```

Application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin: http://localhost:8000/admin

## API Key Setup

### Bright Data
1. Sign up at https://www.brightdata.com
2. Get SERP API key
3. Set `BRIGHT_DATA_API_KEY` in .env

### OpenAI
1. Sign up at https://openai.com
2. Generate API key from https://platform.openai.com/account/api-keys
3. Set `OPENAI_API_KEY` in .env

## Development Workflow

### Adding a New API Endpoint

1. **Create Model** (api/models.py)
   ```python
   class YourModel(models.Model):
       name = models.CharField(max_length=255)
       # ... more fields
   ```

2. **Create Serializer** (api/serializers.py)
   ```python
   class YourModelSerializer(serializers.ModelSerializer):
       class Meta:
           model = YourModel
           fields = ['id', 'name', ...]
   ```

3. **Create ViewSet** (api/views.py)
   ```python
   class YourModelViewSet(viewsets.ModelViewSet):
       queryset = YourModel.objects.all()
       serializer_class = YourModelSerializer
   ```

4. **Register URL** (api/urls.py)
   ```python
   router.register(r'yourmodel', views.YourModelViewSet)
   ```

### Testing

```bash
# Backend tests
cd backend
python manage.py test api

# Frontend tests
cd frontend
npm test
```

## Common Issues

### Issue: ModuleNotFoundError
**Solution**: Make sure venv is activated and dependencies are installed
```bash
source venv/Scripts/activate
pip install -r requirements.txt
```

### Issue: Database connection error
**Solution**: Check PostgreSQL is running and .env credentials are correct
```bash
# Check PostgreSQL
psql -U postgres
\l  # List databases
```

### Issue: CORS errors
**Solution**: Make sure CORS_ALLOWED_ORIGINS includes frontend URL in settings.py

### Issue: React can't connect to API
**Solution**: Check REACT_APP_API_URL in .env and that backend is running

## Next Steps

1. Set up Bright Data API integration
2. Test SERP API calls
3. Create initial scrapers for Steam data
4. Connect OpenAI for analysis
5. Build dashboard UI components
6. Create demo data workflow
