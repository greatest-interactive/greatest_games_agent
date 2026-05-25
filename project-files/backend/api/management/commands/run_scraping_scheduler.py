"""
Management command to run automatic game scraping
This command can be scheduled to run periodically via cron or task scheduler

Usage:
    python manage.py run_scraping_scheduler
    python manage.py run_scraping_scheduler --force
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from api.models import ScrapingJob, Game, Competitor
from api.services.bright_data import bright_data_client
import logging
import uuid

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run automatic game scraping scheduler'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force scraping regardless of last run time'
        )
        parser.add_argument(
            '--source',
            type=str,
            help='Specific source to scrape (steam, epic, itch_io)',
            default='all'
        )
    
    def handle(self, *args, **options):
        force = options['force']
        source = options['source']
        
        self.stdout.write(self.style.SUCCESS('Starting automatic scraping scheduler...'))
        
        try:
            # Scrape games
            if source == 'all' or source == 'steam':
                self.scrape_platform('steam', force)
            
            if source == 'all' or source == 'epic':
                self.scrape_platform('epic', force)
            
            if source == 'all' or source == 'itch_io':
                self.scrape_platform('itch_io', force)
            
            # Update competitor data
            if source == 'all':
                self.update_competitors()
            
            self.stdout.write(self.style.SUCCESS('Scraping scheduler completed successfully!'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            logger.error(f'Scraping scheduler error: {str(e)}')
    
    def scrape_platform(self, platform, force=False):
        """Scrape a specific platform"""
        job = None
        try:
            # Check if we should scrape based on platform schedule
            try:
                last_job = ScrapingJob.objects.filter(source=platform, status='completed').latest('created_at')
                
                # Check intervals based on platform
                if platform == 'steam' and not force:
                    interval = timedelta(hours=12)
                elif platform == 'epic' and not force:
                    interval = timedelta(hours=12)
                elif platform == 'itch_io' and not force:
                    interval = timedelta(days=1)
                else:
                    interval = timedelta(hours=1)
                
                if not force and timezone.now() - last_job.created_at < interval:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Skipping {platform}: Last scrape was too recent'
                        )
                    )
                    return
            
            except ScrapingJob.DoesNotExist:
                pass
            
            self.stdout.write(f'Scraping {platform}...')
            
            # Create scraping job with unique job_id
            job = ScrapingJob.objects.create(
                job_id=f'{platform}_{timezone.now().timestamp()}_{uuid.uuid4().hex[:8]}',
                source=platform,
                status='running',
                query=f'popular games on {platform}'
            )
            
            # Get games based on platform
            games_data = []
            
            if platform == 'steam' and bright_data_client:
                result = bright_data_client.scrape_steam_trending()
                if result and result.get('status') == 'success':
                    games_data = result.get('games', [])
            
            elif platform == 'epic' and bright_data_client:
                # For Epic, use SERP search as scraper doesn't have specific method
                result = bright_data_client.search_serp('best games on epic games store 2026', {'limit': 50})
                if result and 'results' in result:
                    games_data = result.get('results', [])
            
            elif platform == 'itch_io' and bright_data_client:
                result = bright_data_client.scrape_itch_io_trending()
                if result and result.get('status') == 'success':
                    games_data = result.get('games', [])
            
            # If no data from API, generate mock data for testing
            if not games_data:
                games_data = self._generate_mock_games(platform)
                self.stdout.write(self.style.WARNING(f'Using mock data for {platform} (API unavailable)'))
            
            created_count = 0
            for game_data in games_data:
                try:
                    # Ensure we have basic fields
                    url = game_data.get('url') or game_data.get('link') or f'{platform}_{game_data.get("id", game_data.get("title", "unknown"))}'
                    title = game_data.get('title', game_data.get('name', 'Unknown'))
                    
                    # Skip if no URL or title
                    if not title or not url:
                        continue
                    
                    game, created = Game.objects.update_or_create(
                        url=url,
                        defaults={
                            'title': title,
                            'developer': game_data.get('developer', game_data.get('author', 'Unknown')),
                            'description': game_data.get('description', game_data.get('snippet', '')),
                            'price': float(game_data.get('price', 0)) if game_data.get('price') else None,
                            'rating': float(game_data.get('rating', 0)) if game_data.get('rating') else None,
                            'review_count': int(game_data.get('review_count', game_data.get('reviews', 0))),
                            'platform': platform,
                            'genre': game_data.get('genres', game_data.get('genre', [])),
                            'tags': game_data.get('tags', []),
                            'release_date': game_data.get('release_date'),
                            'scraped_data': game_data,
                        }
                    )
                    if created:
                        created_count += 1
                except Exception as e:
                    logger.warning(f"Error saving game from {platform}: {str(e)}")
            
            job.status = 'completed'
            job.results_count = created_count
            job.completed_at = timezone.now()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ {platform}: Added {created_count} games'
                )
            )
        
        except Exception as e:
            error_msg = f'Error scraping {platform}: {str(e)}'
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(error_msg)
            
            if job:
                job.status = 'failed'
                job.error_message = str(e)
                job.completed_at = timezone.now()
        
        finally:
            if job:
                job.save()
    
    def _generate_mock_games(self, platform):
        """Generate mock game data for testing when API is unavailable"""
        mock_games_data = {
            'steam': [
                {
                    'id': 'steam_001',
                    'title': 'Cyberpunk Noir',
                    'author': 'Neo Studios',
                    'price': 49.99,
                    'rating': 8.5,
                    'reviews': 15230,
                    'genre': ['Action', 'RPG'],
                    'description': 'Immersive cyberpunk adventure with noir aesthetic',
                    'url': 'https://steampowered.com/app/cyberpunk_noir'
                },
                {
                    'id': 'steam_002',
                    'title': 'Cosmic Explorer',
                    'author': 'Stellar Games',
                    'price': 29.99,
                    'rating': 9.0,
                    'reviews': 8456,
                    'genre': ['Sci-Fi', 'Adventure'],
                    'description': 'Explore distant galaxies in this space adventure',
                    'url': 'https://steampowered.com/app/cosmic_explorer'
                },
            ],
            'epic': [
                {
                    'id': 'epic_001',
                    'title': 'Enchanted Realm',
                    'author': 'Fantasy Games Inc',
                    'price': 39.99,
                    'rating': 8.7,
                    'reviews': 12000,
                    'genre': ['Fantasy', 'RPG'],
                    'description': 'Magic-filled fantasy world with epic quests',
                    'url': 'https://epicgames.com/store/enchanted_realm'
                },
                {
                    'id': 'epic_002',
                    'title': 'Racing Thunder',
                    'author': 'Speed Studios',
                    'price': 34.99,
                    'rating': 8.2,
                    'reviews': 9876,
                    'genre': ['Racing', 'Sports'],
                    'description': 'High-octane racing with realistic physics',
                    'url': 'https://epicgames.com/store/racing_thunder'
                },
            ],
            'itch_io': [
                {
                    'id': 'itch_001',
                    'title': 'Pixel Quest',
                    'author': 'Indie Dev Collective',
                    'price': 9.99,
                    'rating': 8.9,
                    'reviews': 5432,
                    'genre': ['Indie', 'Adventure'],
                    'description': 'Charming pixel art adventure game',
                    'url': 'https://itch.io/games/pixel_quest'
                },
                {
                    'id': 'itch_002',
                    'title': 'Neon Nights',
                    'author': 'Neon Studios',
                    'price': 7.99,
                    'rating': 8.4,
                    'reviews': 3210,
                    'genre': ['Indie', 'Action'],
                    'description': 'Synthwave-inspired action platformer',
                    'url': 'https://itch.io/games/neon_nights'
                },
            ]
        }
        
        return mock_games_data.get(platform, [])
    
    def update_competitors(self):
        """Update competitor data from scraped games"""
        self.stdout.write('Updating competitor data...')
        
        try:
            # Get recent games
            recent_games = Game.objects.order_by('-updated_at')[:30]
            
            updated_count = 0
            for game in recent_games:
                try:
                    comp, created = Competitor.objects.update_or_create(
                        game_title=game.title,
                        platform=game.platform,
                        defaults={
                            'developer': game.developer,
                            'genre': ', '.join(game.genre) if isinstance(game.genre, list) else str(game.genre),
                            'price': game.price,
                            'rating': game.rating,
                            'review_count': game.review_count,
                            'url': game.url,
                        }
                    )
                    updated_count += 1
                except Exception as e:
                    logger.warning(f"Error updating competitor for {game.title}: {str(e)}")
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Updated {updated_count} competitor entries')
            )
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating competitors: {str(e)}'))
            logger.error(f'Error updating competitors: {str(e)}')
