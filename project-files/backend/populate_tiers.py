#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greatest_game_agent.settings')
django.setup()

from api.models import Tier

# Delete existing tiers
Tier.objects.all().delete()

# Create tiers
tiers_data = [
    {
        'name': 'free',
        'display_name': 'Free',
        'description': 'Get started with limited access to all features',
        'price_monthly': 0,
        'monthly_tokens': 50,
        'max_saved_games': 5,
        'max_api_requests_per_day': 100,
        'max_scraping_jobs': 1,
        'features': [
            'Basic game tracking',
            'Limited trend analysis',
            'Community support',
            '5 saved games',
            '50 monthly tokens'
        ]
    },
    {
        'name': 'starter',
        'display_name': 'Starter - $9.99/mo',
        'description': 'Scale your game development with advanced tools',
        'price_monthly': 9.99,
        'price_yearly': 99.90,
        'monthly_tokens': 500,
        'max_saved_games': 50,
        'max_api_requests_per_day': 500,
        'max_scraping_jobs': 5,
        'features': [
            'All Free features',
            'Advanced market analysis',
            'Competitor tracking',
            '50 saved games',
            '500 monthly tokens',
            'Email support',
            'Batch scraping'
        ]
    },
    {
        'name': 'pro',
        'display_name': 'Pro - $29.99/mo',
        'description': 'Professional tools for game studios and analysts',
        'price_monthly': 29.99,
        'price_yearly': 299.90,
        'monthly_tokens': 2000,
        'max_saved_games': 999999,
        'max_api_requests_per_day': 2000,
        'max_scraping_jobs': 20,
        'features': [
            'All Starter features',
            'Unlimited saved games',
            'Real-time data updates',
            'Advanced AI predictions',
            '2000 monthly tokens',
            'Priority support',
            'Custom API endpoints',
            'Data export (CSV/JSON)',
            'Team collaboration (2 users)'
        ]
    },
    {
        'name': 'enterprise',
        'display_name': 'Enterprise',
        'description': 'Custom solutions for large-scale operations',
        'price_monthly': 0,
        'monthly_tokens': 99999,
        'max_saved_games': 999999,
        'max_api_requests_per_day': 99999,
        'max_scraping_jobs': 100,
        'features': [
            'All Pro features',
            'Unlimited everything',
            'Dedicated account manager',
            'Custom integrations',
            'On-premise deployment',
            'SLA guarantees',
            'Unlimited users',
            'Advanced analytics & reporting',
            'Custom AI models',
            '24/7 phone support'
        ]
    }
]

for tier_data in tiers_data:
    Tier.objects.create(**tier_data)
    print(f"Created tier: {tier_data['display_name']}")

print(f"\nSuccessfully created {Tier.objects.count()} tiers")
