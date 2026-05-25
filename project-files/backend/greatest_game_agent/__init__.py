# Greatest Game Agent

# Optional Celery app initialization
# Only imports if celery is available (for production use)
# For development, use: python manage.py run_scraping_scheduler
try:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
except ImportError:
    # Celery not installed, using management command for scraping instead
    pass
