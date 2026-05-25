"""
WSGI config for Greatest Game Agent project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greatest_game_agent.settings')

application = get_wsgi_application()
