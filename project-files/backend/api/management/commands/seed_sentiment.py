from django.core.management.base import BaseCommand
from api.models import PlayerSentiment
import random


class Command(BaseCommand):
    help = 'Populate database with player sentiment data'

    def handle(self, *args, **options):
        # Clear existing sentiment
        PlayerSentiment.objects.all().delete()

        sentiment_data = [
            # Positive sentiments
            {
                'game_title': 'Balatro',
                'sentiment_type': 'positive',
                'source': 'steam',
                'sentiment_score': 0.95,
                'comment': 'Absolutely addictive poker roguelike! One of the best indie games ever. Cannot put it down, 100+ hours already.',
                'key_themes': ['addictive', 'fun', 'replay-value', 'unique'],
                'engagement_metric': 2540,
                'url': 'https://steamcommunity.com/app/balatro'
            },
            {
                'game_title': 'Balatro',
                'sentiment_type': 'positive',
                'source': 'reddit',
                'sentiment_score': 0.92,
                'comment': 'Balatro has taken over my life in the best way possible. The learning curve is perfect and progression feels rewarding.',
                'key_themes': ['rewarding', 'progression', 'learning-curve', 'perfect'],
                'engagement_metric': 8340,
                'url': 'https://reddit.com/r/indiegaming'
            },
            {
                'game_title': 'Hollow Knight',
                'sentiment_type': 'positive',
                'source': 'youtube',
                'sentiment_score': 0.89,
                'comment': 'Masterpiece of game design. The art, music, and level design are all exceptional. Boss fights are challenging but fair.',
                'key_themes': ['masterpiece', 'art', 'music', 'challenging', 'fair'],
                'engagement_metric': 45000,
                'url': 'https://youtube.com/watch?v=...'
            },
            {
                'game_title': 'Elden Ring',
                'sentiment_type': 'positive',
                'source': 'steam',
                'sentiment_score': 0.87,
                'comment': 'FromSoftware nailed the open world formula. Freedom to explore + challenging combat = perfection. GOTY contender.',
                'key_themes': ['open-world', 'freedom', 'challenging', 'goty'],
                'engagement_metric': 12340,
                'url': 'https://steamcommunity.com/app/elden-ring'
            },
            {
                'game_title': 'Baldurs Gate 3',
                'sentiment_type': 'positive',
                'source': 'reddit',
                'sentiment_score': 0.93,
                'comment': 'BG3 set a new standard for RPGs. Story choices feel meaningful and there are countless playstyle options.',
                'key_themes': ['choice', 'meaningful', 'rpg', 'replayable'],
                'engagement_metric': 15600,
                'url': 'https://reddit.com/r/baldursgate3'
            },
            # Neutral sentiments
            {
                'game_title': 'Starfield',
                'sentiment_type': 'neutral',
                'source': 'steam',
                'sentiment_score': 0.15,
                'comment': 'Starfield is a solid space game but feels a bit dated in some aspects. Good exploration but content is scattered.',
                'key_themes': ['exploration', 'dated', 'scattered', 'mixed'],
                'engagement_metric': 3200,
                'url': 'https://steamcommunity.com/app/starfield'
            },
            {
                'game_title': 'Call of Duty Modern Warfare 3',
                'sentiment_type': 'neutral',
                'source': 'youtube',
                'sentiment_score': 0.22,
                'comment': 'CoD MW3 is more of the same. Fun multiplayer but nothing revolutionary. Annual releases are tiring.',
                'key_themes': ['samey', 'multiplayer', 'annual-release', 'uninspired'],
                'engagement_metric': 28000,
                'url': 'https://youtube.com/watch?v=...'
            },
            {
                'game_title': 'Final Fantasy XVI',
                'sentiment_type': 'neutral',
                'source': 'discord',
                'sentiment_score': 0.35,
                'comment': 'FF16 has great combat and visuals but the story is convoluted. Some side quests feel like filler.',
                'key_themes': ['story', 'combat', 'filler', 'mixed-quality'],
                'engagement_metric': 4500,
                'url': 'https://discord.gg/finalfantasy'
            },
            # Negative sentiments
            {
                'game_title': 'Diablo Immortal',
                'sentiment_type': 'negative',
                'source': 'reddit',
                'sentiment_score': -0.88,
                'comment': 'Diablo Immortal is a p2w nightmare. Predatory monetization ruined what could have been a great mobile game.',
                'key_themes': ['pay-to-win', 'predatory', 'monetization', 'disappointment'],
                'engagement_metric': 9200,
                'url': 'https://reddit.com/r/diabloimmortal'
            },
            {
                'game_title': 'Concord',
                'sentiment_type': 'negative',
                'source': 'steam',
                'sentiment_score': -0.82,
                'comment': 'Another failed hero shooter. Already feeling dead on arrival. Queue times are terrible.',
                'key_themes': ['dead-game', 'hero-shooter', 'poor-launch', 'no-players'],
                'engagement_metric': 1200,
                'url': 'https://steamcommunity.com/app/concord'
            },
            {
                'game_title': 'Microsoft Flight Simulator 2024',
                'sentiment_type': 'negative',
                'source': 'youtube',
                'sentiment_score': -0.45,
                'comment': 'Flight Sim 2024 has optimization issues and performance is unacceptable. Great potential ruined by bugs.',
                'key_themes': ['bugs', 'performance', 'optimization', 'wasted-potential'],
                'engagement_metric': 32000,
                'url': 'https://youtube.com/watch?v=...'
            },
            # More positive sentiments for trending games
            {
                'game_title': 'Celeste',
                'sentiment_type': 'positive',
                'source': 'reddit',
                'sentiment_score': 0.91,
                'comment': 'Celeste combines challenging platforming with heartfelt storytelling. The mental health themes resonate deeply.',
                'key_themes': ['platformer', 'story', 'emotional', 'challenging'],
                'engagement_metric': 7840,
                'url': 'https://reddit.com/r/CelesteGame'
            },
            {
                'game_title': 'Hades',
                'sentiment_type': 'positive',
                'source': 'steam',
                'sentiment_score': 0.94,
                'comment': 'Hades proves roguelikes can have exceptional story and character development. Each run feels fresh and rewarding.',
                'key_themes': ['roguelike', 'story', 'characters', 'replayable'],
                'engagement_metric': 18900,
                'url': 'https://steamcommunity.com/app/hades'
            },
            {
                'game_title': 'Palworld',
                'sentiment_type': 'positive',
                'source': 'youtube',
                'sentiment_score': 0.85,
                'comment': 'Palworld is a wild ride - Pokemon meets survival crafting. Chaotic fun with friends and surprisingly deep mechanics.',
                'key_themes': ['fun', 'multiplayer', 'crafting', 'pokemon-inspired'],
                'engagement_metric': 156000,
                'url': 'https://youtube.com/watch?v=...'
            },
            {
                'game_title': 'Dave the Diver',
                'sentiment_type': 'positive',
                'source': 'tiktok',
                'sentiment_score': 0.90,
                'comment': 'Dave the Diver is a hidden gem! Charming, relaxing, yet surprisingly engaging. Best free game ever made.',
                'key_themes': ['charming', 'relaxing', 'gem', 'free'],
                'engagement_metric': 245000,
                'url': 'https://tiktok.com/...'
            },
            {
                'game_title': 'Helldivers 2',
                'sentiment_type': 'positive',
                'source': 'reddit',
                'sentiment_score': 0.89,
                'comment': 'Helldivers 2 nailed co-op gameplay. Hilarious chaos with friends and genuinely challenging missions. Worth every penny.',
                'key_themes': ['coop', 'challenging', 'fun', 'community'],
                'engagement_metric': 12300,
                'url': 'https://reddit.com/r/Helldivers'
            },
        ]

        for sentiment in sentiment_data:
            PlayerSentiment.objects.create(**sentiment)
            self.stdout.write(self.style.SUCCESS(f"Created sentiment: {sentiment['game_title']} - {sentiment['sentiment_type']}"))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully populated {len(sentiment_data)} sentiment entries'))
