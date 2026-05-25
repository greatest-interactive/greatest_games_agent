"""
Optional Celery configuration for Greatest Game Agent
This is only needed if you want to use Celery for background task scheduling

For development/simple deployment, use:
    python manage.py run_scraping_scheduler

For production with Redis and Celery:
    1. Install: pip install celery[redis] django-celery-beat redis
    2. Start worker: celery -A greatest_game_agent worker -l info
    3. Start beat: celery -A greatest_game_agent beat -l info
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greatest_game_agent.settings')

app = Celery('greatest_game_agent')

# Load config from Django settings (requires django-celery-beat to be installed)
try:
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()
    
    # Celery Beat Schedule for periodic tasks (optional, only if Celery is used)
    app.conf.beat_schedule = {
        'scrape-games-every-hour': {
            'task': 'api.tasks.scrape_games_periodic',
            'schedule': crontab(minute=0),  # Every hour
        },
    }
except Exception:
    # Celery not properly configured, falling back to management command approach
    pass

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
