"""
Optional Celery tasks for Greatest Game Agent
These tasks are only used if Celery and Redis are installed and configured.

For development and simple deployments, use the management command instead:
    python manage.py run_scraping_scheduler

This file is kept for reference in case you want to set up Celery in the future.
"""

# Celery tasks are optional and only loaded if Celery is properly configured
# For now, use: python manage.py run_scraping_scheduler
