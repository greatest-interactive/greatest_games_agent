"""
Bright Data Integration Service

Handles all interactions with Bright Data APIs:
- SERP API for trending searches
- Web Scraper API for marketplace scraping
- Scraping Browser for dynamic content
"""

import requests
import json
import logging
from typing import Dict, List, Optional
from decouple import config

logger = logging.getLogger(__name__)

BRIGHT_DATA_API_KEY = config('BRIGHT_DATA_API_KEY', default='')
BRIGHT_DATA_BASE_URL = 'https://api.brightdata.com'


class BrightDataClient:
    """Client for Bright Data APIs"""
    
    def __init__(self, api_key: str = BRIGHT_DATA_API_KEY):
        self.api_key = api_key
        self.base_url = BRIGHT_DATA_BASE_URL
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
    
    def search_serp(self, query: str, location: str = 'US', language: str = 'en') -> Optional[Dict]:
        """
        Search using Bright Data SERP API
        
        Returns top search results for gaming trends
        Example: "horror games 2026", "best indie platformers"
        """
        try:
            endpoint = f'{self.base_url}/serp'
            payload = {
                'query': query,
                'country': location,
                'language': language,
                'results_language': language,
            }
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f'SERP search successful for: {query}')
                return {
                    'query': query,
                    'results': data.get('results', []),
                    'organic_results': data.get('organic_results', []),
                    'status': 'success',
                }
            else:
                logger.error(f'SERP API error: {response.status_code} - {response.text}')
                return None
                
        except Exception as e:
            logger.error(f'SERP search error: {str(e)}')
            return None
    
    def scrape_steam_trending(self) -> Optional[Dict]:
        """
        Scrape Steam trending games page
        Returns: List of trending games with reviews, pricing, tags
        """
        try:
            endpoint = f'{self.base_url}/scraper'
            payload = {
                'url': 'https://steampowered.com/search/?os=win&deck_show_exclude=1',
                'parser': 'steam_search',
                'format': 'json',
            }
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info('Steam scraping successful')
                return {
                    'source': 'Steam',
                    'games': data.get('results', []),
                    'status': 'success',
                }
            else:
                logger.error(f'Steam scraper error: {response.status_code}')
                return None
                
        except Exception as e:
            logger.error(f'Steam scraping error: {str(e)}')
            return None
    
    def scrape_itch_io_trending(self) -> Optional[Dict]:
        """
        Scrape itch.io trending games
        Returns: List of indie games with ratings, downloads, genres
        """
        try:
            endpoint = f'{self.base_url}/scraper'
            payload = {
                'url': 'https://itch.io/games/trending',
                'parser': 'itch_io_trending',
                'format': 'json',
            }
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info('itch.io scraping successful')
                return {
                    'source': 'itch.io',
                    'games': data.get('results', []),
                    'status': 'success',
                }
            else:
                logger.error(f'itch.io scraper error: {response.status_code}')
                return None
                
        except Exception as e:
            logger.error(f'itch.io scraping error: {str(e)}')
            return None
    
    def search_trending_terms(self, category: str = 'games') -> Optional[Dict]:
        """
        Search for trending terms in gaming category
        Uses SERP API to find what people are searching for
        """
        trending_queries = [
            f'best {category} 2026',
            f'upcoming {category}',
            f'free {category}',
            f'indie {category}',
            f'horror {category}',
            f'multiplayer {category}',
        ]
        
        all_results = []
        for query in trending_queries:
            result = self.search_serp(query)
            if result:
                all_results.append(result)
        
        return {
            'trending_searches': all_results,
            'status': 'success' if all_results else 'partial',
        }
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """
        Get status of a scraping job
        """
        try:
            endpoint = f'{self.base_url}/scraper/status/{job_id}'
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f'Status check error: {response.status_code}')
                return None
                
        except Exception as e:
            logger.error(f'Status check error: {str(e)}')
            return None


# Initialize client
bright_data_client = BrightDataClient()
