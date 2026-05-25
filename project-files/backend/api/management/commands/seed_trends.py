from django.core.management.base import BaseCommand
from api.models import Trend
from datetime import datetime


class Command(BaseCommand):
    help = 'Populate database with realistic gaming trends data'

    def handle(self, *args, **options):
        # Clear existing trends
        Trend.objects.all().delete()

        trends_data = [
            # Genres
            {
                'title': 'Roguelike/Roguelite Games',
                'category': 'genre',
                'description': 'Games with procedural generation and permanent death mechanics continue to dominate indie and AAA markets. Titles like Hades, Hollow Knight, and Balatro prove this genre has staying power.',
                'keywords': ['roguelike', 'procedural', 'permadeath', 'indie', 'loop-based'],
                'momentum_score': 92.5,
                'growth_rate': 23.4,
                'search_volume': 185000,
                'opportunity_level': 'high',
                'market_gap': 'Roguelikes with strong narrative focus in mid-core market',
                'supporting_data': {
                    'top_games': ['Hades', 'Hollow Knight', 'Balatro', 'Dead Cells'],
                    'avg_rating': 8.6,
                    'market_size_millions': 450
                }
            },
            {
                'title': 'Indie Puzzle Games',
                'category': 'genre',
                'description': 'Puzzle games from indie developers seeing massive growth on platforms like Steam and App Store. Casual players increasingly seeking brain-teasing experiences.',
                'keywords': ['puzzle', 'indie', 'casual', 'brain-teaser', 'logic'],
                'momentum_score': 78.3,
                'growth_rate': 18.7,
                'search_volume': 124000,
                'opportunity_level': 'high',
                'market_gap': 'Multiplayer puzzle experiences, puzzle-roguelike hybrids',
                'supporting_data': {
                    'top_games': ['The Witness', 'Tetris Effect', 'Portal', 'Baba Is You'],
                    'avg_rating': 8.2,
                    'market_size_millions': 280
                }
            },
            {
                'title': 'Action Adventure',
                'category': 'genre',
                'description': 'Metroidvania and action-adventure games maintaining strong momentum across consoles and PC. Exploration and combat systems define this evergreen genre.',
                'keywords': ['metroidvania', 'exploration', 'combat', 'adventure', 'action'],
                'momentum_score': 85.2,
                'growth_rate': 15.3,
                'search_volume': 156000,
                'opportunity_level': 'medium',
                'market_gap': 'Story-driven action adventure, indie-AAA hybrid experiences',
                'supporting_data': {
                    'top_games': ['Elden Ring', 'Zelda Tears of Kingdom', 'Dead Space Remake'],
                    'avg_rating': 8.4,
                    'market_size_millions': 720
                }
            },
            # Mechanics
            {
                'title': 'Procedural Generation',
                'category': 'mechanic',
                'description': 'Procedural level generation and content creation continues to be a key mechanic in successful indie games. Enables infinite replayability and reduces development costs.',
                'keywords': ['procedural', 'generation', 'infinite-replayability', 'ai-content', 'automation'],
                'momentum_score': 88.4,
                'growth_rate': 31.2,
                'search_volume': 95000,
                'opportunity_level': 'high',
                'market_gap': 'Procedural generation + AI narrative integration',
                'supporting_data': {
                    'adoption_rate': '64% of indie games',
                    'player_preference': '72% prefer procedural over hand-crafted',
                    'development_time_saved': '35-50%'
                }
            },
            {
                'title': 'Cross-Platform Play',
                'category': 'mechanic',
                'description': 'Cross-platform multiplayer and cloud save features now expected in modern games. Players demand seamless switching between devices.',
                'keywords': ['cross-platform', 'multiplayer', 'cloud-save', 'seamless', 'device-agnostic'],
                'momentum_score': 82.1,
                'growth_rate': 28.5,
                'search_volume': 142000,
                'opportunity_level': 'high',
                'market_gap': 'Cross-platform competitive experiences with fair balance',
                'supporting_data': {
                    'player_expectation': '81% expect cross-platform',
                    'implementation_ease': 'Medium with right tools',
                    'retention_boost': '+25% average'
                }
            },
            {
                'title': 'Real-Time Strategy Elements',
                'category': 'mechanic',
                'description': 'RTS mechanics integrated into genre-diverse games. Base building, resource management, and tactical decision-making appeal to strategic players.',
                'keywords': ['rts', 'base-building', 'resource-management', 'strategy', 'tactics'],
                'momentum_score': 71.5,
                'growth_rate': 19.8,
                'search_volume': 78000,
                'opportunity_level': 'medium',
                'market_gap': 'Casual-friendly RTS with short play sessions',
                'supporting_data': {
                    'games_using': ['StarCraft', 'They Are Billions', 'Northgard'],
                    'session_length': '15-45 minutes',
                    'core_demographic': 'Age 20-35'
                }
            },
            # Monetization
            {
                'title': 'Battle Pass Systems',
                'category': 'monetization',
                'description': 'Battle passes dominating monetization across multiplayer games. Seasonal progression and cosmetics driving recurring revenue. Players appreciate structured progression paths.',
                'keywords': ['battle-pass', 'seasonal', 'cosmetics', 'progression', 'recurring-revenue'],
                'momentum_score': 91.3,
                'growth_rate': 42.1,
                'search_volume': 210000,
                'opportunity_level': 'high',
                'market_gap': 'Single-player battle pass experiences without competitive pressure',
                'supporting_data': {
                    'avg_price': '$9.99-$19.99',
                    'completion_rate': '35-45%',
                    'revenue_per_user': '$3.50 avg'
                }
            },
            {
                'title': 'Premium Cosmetics & Skins',
                'category': 'monetization',
                'description': 'Premium cosmetic items (skins, emotes, effects) generating majority of non-pay-to-win revenue. Players willing to spend for visual customization and status symbols.',
                'keywords': ['cosmetics', 'skins', 'premium', 'vanity', 'customization'],
                'momentum_score': 86.7,
                'growth_rate': 35.8,
                'search_volume': 165000,
                'opportunity_level': 'high',
                'market_gap': 'Cosmetics with lore-driven collection narratives',
                'supporting_data': {
                    'avg_item_price': '$5-$30',
                    'repeat_purchase_rate': '28%',
                    'player_satisfaction': '84% approve cosmetic monetization'
                }
            },
            {
                'title': 'Subscription Services',
                'category': 'monetization',
                'description': 'Game subscription services (PlayStation Plus, Game Pass) influencing game design. Multiple revenue streams becoming industry standard.',
                'keywords': ['subscription', 'game-pass', 'recurring', 'subscription-service', 'membership'],
                'momentum_score': 79.2,
                'growth_rate': 22.3,
                'search_volume': 132000,
                'opportunity_level': 'medium',
                'market_gap': 'Indie games on subscription services, subscription-exclusive titles',
                'supporting_data': {
                    'subscribers_millions': 45,
                    'revenue_per_user': '$12.99/month avg',
                    'churn_rate': '8% monthly'
                }
            },
            # Aesthetics & Technology
            {
                'title': '2D Pixel Art Renaissance',
                'category': 'aesthetic',
                'description': 'Pixel art and retro aesthetics experiencing resurgence with indie developers. Proves that visual fidelity is not essential for success and engaging gameplay.',
                'keywords': ['pixel-art', 'retro', '2d', 'indie', 'pixel-graphics'],
                'momentum_score': 84.5,
                'growth_rate': 26.7,
                'search_volume': 118000,
                'opportunity_level': 'medium',
                'market_gap': 'High-quality pixel art with modern UI/UX design',
                'supporting_data': {
                    'successful_games': ['Celeste', 'Shovel Knight', 'Hyper Light Drifter'],
                    'development_cost_reduction': '50-70%',
                    'artistic_appeal': 'Timeless'
                }
            },
            {
                'title': 'Ray Tracing & Advanced Graphics',
                'category': 'aesthetic',
                'description': 'Next-gen graphics with ray tracing becoming standard for AAA titles on new consoles. Immersive visual experiences driving hardware upgrades.',
                'keywords': ['ray-tracing', 'graphics', 'realistic', 'visual-fidelity', 'next-gen'],
                'momentum_score': 76.8,
                'growth_rate': 15.2,
                'search_volume': 145000,
                'opportunity_level': 'medium',
                'market_gap': 'Ray tracing on budget hardware, real-time ray tracing in mobile',
                'supporting_data': {
                    'adoption_rate': '45% of AAA games',
                    'performance_impact': '10-40% FPS reduction',
                    'player_preference': '68% prefer visual quality over FPS'
                }
            },
        ]

        for trend_data in trends_data:
            Trend.objects.create(**trend_data)
            self.stdout.write(self.style.SUCCESS(f"Created trend: {trend_data['title']}"))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully populated {len(trends_data)} trends'))
