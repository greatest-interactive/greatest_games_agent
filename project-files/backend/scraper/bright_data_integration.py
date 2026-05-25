"""
Bright Data integration module for Greatest Game Agent.
Handles API calls to Bright Data services.
"""
import requests
import json
from typing import Dict, List, Any
from django.conf import settings


class BrightDataClient:
    """Client for interacting with Bright Data APIs."""
    
    def __init__(self):
        self.api_key = settings.BRIGHT_DATA_API_KEY
        self.base_url = "https://api.brightdata.com"
        self.serp_api_url = f"{self.base_url}/serp"
        self.scraper_api_url = f"{self.base_url}/scraper"
    
    def search_serp(self, query: str, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Search using Bright Data SERP API.
        
        Args:
            query: Search query
            filters: Optional filters for the search
            
        Returns:
            Search results
        """
        payload = {
            "query": query,
            "api_key": self.api_key,
        }
        
        if filters:
            payload.update(filters)
        
        try:
            response = requests.post(self.serp_api_url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "results": []}
    
    def scrape_website(self, url: str, selectors: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Scrape a website using Bright Data Web Scraper API.
        
        Args:
            url: Website URL to scrape
            selectors: CSS selectors for specific data
            
        Returns:
            Scraped data
        """
        payload = {
            "url": url,
            "api_key": self.api_key,
        }
        
        if selectors:
            payload["selectors"] = selectors
        
        try:
            response = requests.post(self.scraper_api_url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "data": None}


def fetch_market_data(game_concept: str, genre: str) -> Dict[str, Any]:
    """
    Fetch market data for a game concept using Bright Data.
    
    Args:
        game_concept: Game concept/name
        genre: Game genre
        
    Returns:
        Market data including competitors, trends, and sentiment
    """
    client = BrightDataClient()
    
    market_data = {
        "concept": game_concept,
        "genre": genre,
        "search_trends": [],
        "competitors": [],
        "sentiment": [],
        "market_size": None,
    }
    
    try:
        # Search for trending games in the genre
        search_query = f"best {genre} games 2026"
        search_results = client.search_serp(search_query, {"limit": 50})
        
        if search_results and "results" in search_results:
            market_data["search_trends"] = search_results["results"]
        
        # Scrape Steam for competitor data (example)
        steam_query = f"https://store.steampowered.com/search/?term={genre}"
        # In real implementation, this would use the Scraping Browser
        # steam_data = client.scrape_website(steam_query)
        
    except Exception as e:
        market_data["error"] = str(e)
    
    return market_data


def scrape_steam_trending(hours: int = 24) -> List[Dict[str, Any]]:
    """
    Scrape Steam trending games.
    
    Args:
        hours: Time period in hours
        
    Returns:
        List of trending games
    """
    client = BrightDataClient()
    
    # SERP search for trending Steam games
    search_query = f"top trending steam games last {hours} hours"
    results = client.search_serp(search_query, {"limit": 20})
    
    return results.get("results", []) if results else []


def scrape_itch_io_games(genre: str = None) -> List[Dict[str, Any]]:
    """
    Scrape itch.io games.
    
    Args:
        genre: Optional genre filter
        
    Returns:
        List of games from itch.io
    """
    client = BrightDataClient()
    
    url = f"https://itch.io/games"
    if genre:
        url += f"/tag-{genre}"
    
    # Would use Scraping Browser for dynamic content
    try:
        data = client.scrape_website(url)
        return data.get("data", []) if data else []
    except Exception as e:
        return []


def search_gaming_news(keywords: List[str]) -> List[Dict[str, Any]]:
    """
    Search for gaming news and updates.
    
    Args:
        keywords: List of keywords to search
        
    Returns:
        List of news articles
    """
    client = BrightDataClient()
    
    all_results = []
    for keyword in keywords:
        search_query = f"game news {keyword}"
        results = client.search_serp(search_query, {"limit": 30})
        if results and "results" in results:
            all_results.extend(results["results"])
    
    return all_results
