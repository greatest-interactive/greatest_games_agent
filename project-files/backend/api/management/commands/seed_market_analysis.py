from django.core.management.base import BaseCommand
from api.models import MarketAnalysis


class Command(BaseCommand):
    help = 'Populate database with market analysis data'

    def handle(self, *args, **options):
        # Clear existing analysis
        MarketAnalysis.objects.all().delete()

        analysis_data = [
            {
                'query': 'Indie Roguelike Market 2025',
                'analysis_type': 'market_gap',
                'confidence_score': 92.3,
                'ai_insights': {
                    'overview': 'The indie roguelike market is saturated but profitable. Success requires unique mechanics and strong UX.',
                    'market_size': '$450M annually',
                    'growth_trend': '+23.4% YoY',
                    'key_insight': 'Hybrid genres and cross-platform play are differentiators'
                },
                'trending_mechanics': [
                    'Procedural generation with hand-crafted elements',
                    'Narrative integration in roguelike loops',
                    'Cross-platform save systems',
                    'Accessibility options (difficulty modifiers)'
                ],
                'rising_genres': [
                    'Roguelike Deck-builders (Slay the Spire model)',
                    'Roguelike Adventure Games (Hades model)',
                    'Pixel Art Roguelikes (Celeste model)',
                    'Multiplayer Roguelikes (Helldivers model)'
                ],
                'market_gaps': [
                    'Roguelikes with strong single-player narratives',
                    'Casual-friendly roguelikes for mainstream audiences',
                    'Educational roguelikes (learning + fun)',
                    'VR roguelike experiences'
                ],
                'monetization_opportunities': [
                    'Battle pass with cosmetic rewards',
                    'Premium cosmetics and character skins',
                    'Story DLC with new mechanics',
                    'Early access community building'
                ],
                'raw_data': {
                    'successful_titles': ['Hades', 'Balatro', 'Hollow Knight', 'Dead Cells'],
                    'failed_titles': ['Outriders', 'Anthem (roguelike aspects)'],
                    'avg_playtime_hours': 42.5,
                    'player_retention_90days': '28%'
                }
            },
            {
                'query': 'Puzzle Game Market Analysis',
                'analysis_type': 'trend_analysis',
                'confidence_score': 88.7,
                'ai_insights': {
                    'overview': 'Puzzle games are experiencing growth on casual platforms with lower monetization friction.',
                    'market_size': '$280M annually',
                    'growth_trend': '+18.7% YoY',
                    'key_insight': 'Mobile and browser-based puzzle games have highest engagement'
                },
                'trending_mechanics': [
                    'Real-time vs turn-based puzzle solving',
                    'Physics-based puzzles',
                    'Story-integrated puzzle experiences',
                    'Multiplayer/cooperative puzzle solving'
                ],
                'rising_genres': [
                    'Physics Puzzlers (Portal-like)',
                    'Narrative Puzzles (Outer Wilds-like)',
                    'Match-3 with progression systems',
                    'Pattern Recognition Games'
                ],
                'market_gaps': [
                    'Puzzle games with competitive multiplayer',
                    'Puzzle games + roguelike mechanics',
                    'Educational puzzle games with real learning',
                    'Puzzle games for elderly audience'
                ],
                'monetization_opportunities': [
                    'Ads + premium ad-free option',
                    'Cosmetic themes and visual upgrades',
                    'Hint systems and power-ups',
                    'Subscription for puzzle packs'
                ],
                'raw_data': {
                    'successful_titles': ['Portal', 'Baba Is You', 'Tetris Effect', 'Picross'],
                    'failed_titles': ['Various clones without innovation'],
                    'avg_session_length_minutes': 18,
                    'daily_active_users_peak': '45% of installed base'
                }
            },
            {
                'query': 'Competitor Analysis: Action-Adventure Genre',
                'analysis_type': 'competitor_analysis',
                'confidence_score': 85.4,
                'ai_insights': {
                    'overview': 'Action-adventure remains the most commercially successful genre. Competition from AAA studios is intense.',
                    'market_size': '$720M annually',
                    'growth_trend': '+15.3% YoY',
                    'key_insight': 'Story quality and level design are primary differentiators'
                },
                'trending_mechanics': [
                    'Souls-like combat systems',
                    'Open-world exploration',
                    'Environmental puzzle solving',
                    'Dynamic difficulty scaling'
                ],
                'rising_genres': [
                    'Metroidvania Renaissance (Hollow Knight, Blasphemous)',
                    'Soulslike Action (Elden Ring, Dark Souls)',
                    'Narrative-Heavy Adventure (Uncharted, Last of Us)',
                    'Exploration-Focused Adventure (Outer Wilds, Journey)'
                ],
                'market_gaps': [
                    'Eco-friendly adventure games with environmental themes',
                    'Accessible action-adventure (difficulty options)',
                    'Action-adventure with co-op story mode',
                    'Indie action-adventure in mainstream spotlight'
                ],
                'monetization_opportunities': [
                    'Story DLC with new areas',
                    'Cosmetic outfits and weapons skins',
                    'New Game+ with cosmetic rewards',
                    'Expanded story packs (episodic model)'
                ],
                'raw_data': {
                    'top_competitors': ['Elden Ring', 'Zelda TOTK', 'Baldurs Gate 3', 'Starfield'],
                    'avg_development_cost_millions': 45,
                    'avg_lifespan_months': 18,
                    'player_satisfaction_score': 8.4
                }
            },
            {
                'query': 'Monetization Strategy: Games 2025',
                'analysis_type': 'niche_discovery',
                'confidence_score': 89.2,
                'ai_insights': {
                    'overview': 'Battle passes and cosmetics dominate monetization. Anti-consumer practices increasingly penalized.',
                    'market_size': '$2.4B annually (monetization revenue)',
                    'growth_trend': '+42.1% YoY',
                    'key_insight': 'Player trust = monetization success. Predatory tactics reduce lifetime value.'
                },
                'trending_mechanics': [
                    'Battle pass with cosmetic focus',
                    'Premium cosmetics with lore tie-ins',
                    'Season passes with meaningful content',
                    'F2P friendly monetization'
                ],
                'rising_genres': [
                    'Battle Pass Cosmetics ($9.99-19.99)',
                    'Premium Skins with visual impact ($5-30)',
                    'Battle Pass + Premium Bundle options',
                    'Cosmetic Progression with cosmetic rewards'
                ],
                'market_gaps': [
                    'Fair cosmetics without FOMO mechanics',
                    'Pay-what-you-want cosmetic options',
                    'Community-designed cosmetics revenue share',
                    'Charitable cosmetics (proceeds to charity)'
                ],
                'monetization_opportunities': [
                    'Cross-game cosmetics (account-wide skins)',
                    'Limited cosmetics for legacy players',
                    'Creator cosmetics (profits shared with creators)',
                    'Seasonal cosmetic with story tie-ins'
                ],
                'raw_data': {
                    'avg_battle_pass_price_dollars': 9.99,
                    'completion_rate_percent': 38,
                    'cosmetic_attachment_rate_percent': 45,
                    'revenue_per_active_user_dollars': 3.50,
                    'premium_player_retention_boost_percent': 25
                }
            },
            {
                'query': 'Niche Market: Pixel Art Games',
                'analysis_type': 'niche_discovery',
                'confidence_score': 84.1,
                'ai_insights': {
                    'overview': 'Pixel art is no longer budget-friendly fallback - its an artistic choice. Attracts dedicated communities.',
                    'market_size': '$180M annually',
                    'growth_trend': '+26.7% YoY',
                    'key_insight': 'Pixel art + strong game design = profitable indie formula'
                },
                'trending_mechanics': [
                    'Pixel-perfect collision detection',
                    'Retro-inspired visual effects',
                    'High-fidelity pixel animations',
                    'Pixel art + modern UX design'
                ],
                'rising_genres': [
                    'Pixel Art Metroidvania (Hollow Knight, Blasphemous)',
                    'Pixel Art Roguelike (Celeste, Dead Cells)',
                    'Pixel Art Adventure (Hyper Light Drifter)',
                    'Pixel Art RPG (Omori, Stardew Valley)'
                ],
                'market_gaps': [
                    'Pixel art with ray-tracing effects (hybrid)',
                    'Pixel art multiplayer experiences',
                    'Pixel art educational games',
                    'Pixel art VR games'
                ],
                'monetization_opportunities': [
                    'Pixel art cosmetics and themes',
                    'Story expansions with new pixel content',
                    'Pixel art trading card games',
                    'Cosmetic character skins (pixel variations)'
                ],
                'raw_data': {
                    'development_cost_reduction_percent': 60,
                    'avg_dev_team_size': 3,
                    'time_to_market_months': 8,
                    'success_rate_higher_than_3d_percent': 35
                }
            },
        ]

        for analysis in analysis_data:
            MarketAnalysis.objects.create(**analysis)
            self.stdout.write(self.style.SUCCESS(f"Created analysis: {analysis['query']}"))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully populated {len(analysis_data)} market analyses'))
