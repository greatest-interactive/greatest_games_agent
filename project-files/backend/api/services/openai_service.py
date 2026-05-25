"""
OpenAI Integration Service for Greatest Game Agent

Provides AI-powered analysis, predictions, and strategy generation
using OpenAI GPT-4 or GPT-3.5-turbo models.
"""

from openai import OpenAI
import json
import logging
from typing import Dict, List, Optional, Any
from decouple import config
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Initialize OpenAI API
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')
MODEL = config('OPENAI_MODEL', default='gpt-3.5-turbo')


class OpenAIAnalyzer:
    """AI-powered analyzer using OpenAI"""
    
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = MODEL):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    def _sanitize_cache_key(self, key: str) -> str:
        """Sanitize cache key to be memcached compatible"""
        # Replace spaces, colons, and special characters with underscores
        return key.replace(' ', '_').replace(':', '_').replace('-', '_')
    
    def analyze_trends(self, trends_data: List[Dict], game_concept: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze gaming trends and identify opportunities
        
        Args:
            trends_data: List of trend dictionaries with title, category, momentum_score, etc.
            game_concept: Optional game concept to analyze against trends
        
        Returns:
            Analysis with opportunities, risks, and recommendations
        """
        if not trends_data:
            return {"error": "No trends data provided"}
        
        # Check cache first
        cache_key = self._sanitize_cache_key(f"trend_analysis_{game_concept or 'general'}")
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            prompt = self._build_trend_analysis_prompt(trends_data, game_concept)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert gaming market analyst. Provide insightful analysis with specific recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content
            
            result = {
                "analysis": analysis_text,
                "trending_genres": self._extract_genres(analysis_text, trends_data),
                "market_gaps": self._extract_gaps(analysis_text),
                "opportunities": self._extract_opportunities(analysis_text),
                "risks": self._extract_risks(analysis_text),
                "confidence_score": 85.0,
                "status": "success"
            }
            
            # Cache for 6 hours
            cache.set(cache_key, result, 21600)
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    def analyze_competitors(self, competitors_data: List[Dict], game_genre: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze competitor games and provide intelligence
        
        Args:
            competitors_data: List of competitor game dictionaries
            game_genre: Optional game genre for focused analysis
        
        Returns:
            Competitor analysis with strengths, weaknesses, opportunities
        """
        if not competitors_data:
            return {"error": "No competitor data provided"}
        
        cache_key = self._sanitize_cache_key(f"competitor_analysis_{game_genre or 'general'}")
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            prompt = self._build_competitor_analysis_prompt(competitors_data, game_genre)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert competitive intelligence analyst. Analyze competitors and provide actionable insights."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content
            
            result = {
                "analysis": analysis_text,
                "top_competitors": self._extract_top_competitors(competitors_data),
                "competitive_advantages": self._extract_advantages(analysis_text),
                "differentiation_factors": self._extract_differentiation(analysis_text),
                "pricing_strategy": self._extract_pricing_insight(analysis_text, competitors_data),
                "status": "success"
            }
            
            cache.set(cache_key, result, 21600)
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing competitors: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    def identify_market_gaps(self, trends_data: List[Dict], competitors_data: List[Dict]) -> Dict[str, Any]:
        """
        Identify market gaps and underserved niches
        
        Args:
            trends_data: List of trending games/mechanics
            competitors_data: List of existing competitors
        
        Returns:
            Market gap analysis with opportunities
        """
        cache_key = self._sanitize_cache_key("market_gap_analysis")
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            prompt = self._build_market_gap_prompt(trends_data, competitors_data)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a market research expert specializing in gaming. Identify underserved market segments and opportunities."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content
            
            result = {
                "analysis": analysis_text,
                "market_gaps": self._extract_gaps(analysis_text),
                "underserved_niches": self._extract_niches(analysis_text),
                "opportunity_level": "high",
                "status": "success"
            }
            
            cache.set(cache_key, result, 21600)
            return result
            
        except Exception as e:
            logger.error(f"Error identifying market gaps: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    def generate_launch_strategy(self, game_concept: str, genre: str, target_audience: str, 
                                 trends_data: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive launch strategy for a game concept
        
        Args:
            game_concept: Name/description of the game
            genre: Game genre
            target_audience: Target player demographic
            trends_data: Optional trending data for context
        
        Returns:
            Launch strategy with pricing, marketing, timing recommendations
        """
        try:
            prompt = self._build_launch_strategy_prompt(game_concept, genre, target_audience, trends_data)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a game industry strategist. Create comprehensive, actionable launch strategies."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=2500
            )
            
            strategy_text = response.choices[0].message.content
            
            result = {
                "strategy": strategy_text,
                "game_concept": game_concept,
                "genre": genre,
                "target_audience": target_audience,
                "launch_recommendations": self._extract_recommendations(strategy_text),
                "marketing_channels": self._extract_marketing_channels(strategy_text),
                "pricing_suggestions": self._extract_pricing(strategy_text),
                "best_release_window": self._extract_release_window(strategy_text),
                "confidence_score": 88.0,
                "status": "success"
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating launch strategy: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    def predict_trends(self, historical_trends: List[Dict], timeframe: str = "6 months") -> Dict[str, Any]:
        """
        Predict upcoming gaming trends
        
        Args:
            historical_trends: List of historical trend data
            timeframe: Prediction timeframe (e.g., "6 months", "1 year")
        
        Returns:
            Trend predictions with confidence scores
        """
        cache_key = self._sanitize_cache_key(f"trend_predictions_{timeframe}")
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            prompt = self._build_prediction_prompt(historical_trends, timeframe)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a gaming industry futurist. Predict upcoming trends based on current data and industry patterns."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            prediction_text = response.choices[0].message.content
            
            result = {
                "predictions": prediction_text,
                "predicted_trends": self._extract_predicted_trends(prediction_text),
                "confidence_level": "medium-high",
                "timeframe": timeframe,
                "status": "success"
            }
            
            cache.set(cache_key, result, 43200)  # Cache for 12 hours
            return result
            
        except Exception as e:
            logger.error(f"Error predicting trends: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    def query_ai_agent(self, query: str, context_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        General-purpose AI agent for custom queries
        
        Args:
            query: User's question or request
            context_data: Optional contextual data (trends, competitors, etc.)
        
        Returns:
            AI-generated response
        """
        try:
            prompt = self._build_agent_prompt(query, context_data)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert gaming consultant with deep knowledge of market trends, game design, and industry strategy."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            
            return {
                "response": response_text,
                "query": query,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error in AI agent query: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    # Helper methods for prompt construction
    def _build_trend_analysis_prompt(self, trends_data: List[Dict], game_concept: Optional[str]) -> str:
        trends_str = json.dumps(trends_data[:10], indent=2)  # Limit to 10 for token efficiency
        
        concept_context = f" for a game concept called '{game_concept}'" if game_concept else ""
        
        return f"""Analyze the following gaming trends{concept_context}:

{trends_str}

Provide:
1. Key trending genres and mechanics
2. Market opportunities for new games
3. Identified market gaps
4. Risk factors to consider
5. Specific recommendations

Format your response with clear sections."""
    
    def _build_competitor_analysis_prompt(self, competitors_data: List[Dict], game_genre: Optional[str]) -> str:
        competitors_str = json.dumps(competitors_data[:15], indent=2)
        
        genre_context = f" in the {game_genre} genre" if game_genre else ""
        
        return f"""Analyze these competitor games{genre_context}:

{competitors_str}

Provide:
1. Top performing competitors and why
2. Common pricing strategies
3. Competitive advantages to target
4. Differentiation opportunities
5. Player engagement tactics used
6. Weaknesses in current offerings

Format your response with clear sections."""
    
    def _build_market_gap_prompt(self, trends_data: List[Dict], competitors_data: List[Dict]) -> str:
        return f"""Given these trending games/mechanics:

{json.dumps(trends_data[:5], indent=2)}

And these competitor games:

{json.dumps(competitors_data[:5], indent=2)}

Identify:
1. Underserved market segments
2. Unmet player needs
3. Genre combinations that are under-represented
4. Niche opportunities
5. How to position a new game to fill these gaps"""
    
    def _build_launch_strategy_prompt(self, game_concept: str, genre: str, target_audience: str, 
                                     trends_data: Optional[List[Dict]]) -> str:
        trends_context = ""
        if trends_data:
            trends_context = f"\n\nCurrent market trends:\n{json.dumps(trends_data[:5], indent=2)}"
        
        return f"""Create a comprehensive launch strategy for:

Game: {game_concept}
Genre: {genre}
Target Audience: {target_audience}
{trends_context}

Include:
1. Pre-launch marketing plan
2. Pricing strategy recommendation
3. Best launch window/timing
4. Platform release strategy
5. Community engagement tactics
6. Influencer outreach strategy
7. Post-launch content roadmap
8. Success metrics and KPIs"""
    
    def _build_prediction_prompt(self, historical_trends: List[Dict], timeframe: str) -> str:
        return f"""Based on these current gaming trends:

{json.dumps(historical_trends[:10], indent=2)}

Predict what gaming trends will be popular in the next {timeframe}:

1. Emerging genres
2. New game mechanics
3. Technology trends (graphics, platforms)
4. Monetization models
5. Player preference shifts
6. Market consolidation predictions
7. Opportunities for new entrants"""
    
    def _build_agent_prompt(self, query: str, context_data: Optional[Dict]) -> str:
        context_str = ""
        if context_data:
            if context_data.get('trends'):
                context_str += f"\n\nMarket trends: {json.dumps(context_data['trends'][:5], indent=2)}"
            if context_data.get('competitors'):
                context_str += f"\n\nCompetitor data: {json.dumps(context_data['competitors'][:5], indent=2)}"
        
        return f"""User Query: {query}
{context_str}

Provide a detailed, actionable response based on gaming industry knowledge and the provided context."""
    
    # Helper methods for extracting insights
    def _extract_genres(self, text: str, trends_data: List[Dict]) -> List[str]:
        """Extract trending genres from response"""
        genres = []
        for trend in trends_data:
            if trend.get('category') == 'genre':
                genres.append(trend.get('title', ''))
        return genres[:5]
    
    def _extract_gaps(self, text: str) -> List[str]:
        """Extract market gaps from response"""
        gaps = []
        lines = text.split('\n')
        for line in lines:
            if 'gap' in line.lower() or 'opportunity' in line.lower():
                gaps.append(line.strip())
        return gaps[:5]
    
    def _extract_opportunities(self, text: str) -> List[str]:
        """Extract opportunities from response"""
        return [line.strip() for line in text.split('\n') 
                if 'opportunit' in line.lower()][:5]
    
    def _extract_risks(self, text: str) -> List[str]:
        """Extract risks from response"""
        return [line.strip() for line in text.split('\n') 
                if 'risk' in line.lower() or 'challenge' in line.lower()][:5]
    
    def _extract_top_competitors(self, competitors_data: List[Dict]) -> List[Dict]:
        """Extract top competitors by rating"""
        sorted_comp = sorted(competitors_data, 
                            key=lambda x: x.get('rating', 0), 
                            reverse=True)
        return sorted_comp[:5]
    
    def _extract_advantages(self, text: str) -> List[str]:
        """Extract competitive advantages"""
        return [line.strip() for line in text.split('\n') 
                if 'advantage' in line.lower()][:5]
    
    def _extract_differentiation(self, text: str) -> List[str]:
        """Extract differentiation factors"""
        return [line.strip() for line in text.split('\n') 
                if 'differentiat' in line.lower() or 'unique' in line.lower()][:5]
    
    def _extract_pricing_insight(self, text: str, competitors_data: List[Dict]) -> Dict[str, float]:
        """Extract pricing insights"""
        prices = [c.get('price', 0) for c in competitors_data if c.get('price')]
        return {
            "average_price": sum(prices) / len(prices) if prices else 0,
            "price_range": f"${min(prices)}-${max(prices)}" if prices else "N/A",
            "recommended_strategy": "Analyze text for pricing recommendations"
        }
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract recommendations"""
        return [line.strip() for line in text.split('\n') 
                if 'recommend' in line.lower()][:5]
    
    def _extract_marketing_channels(self, text: str) -> List[str]:
        """Extract marketing channel recommendations"""
        channels = []
        for word in ['twitch', 'youtube', 'tiktok', 'steam', 'discord', 'twitter', 'influencer', 'reddit']:
            if word in text.lower():
                channels.append(word.capitalize())
        return channels
    
    def _extract_pricing(self, text: str) -> Dict[str, Any]:
        """Extract pricing recommendations"""
        return {
            "recommendation": "Review analysis for specific pricing",
            "strategy": "Value-based or market-based pricing"
        }
    
    def _extract_release_window(self, text: str) -> str:
        """Extract recommended release window"""
        return "Review analysis for specific timing recommendations"
    
    def _extract_predicted_trends(self, text: str) -> List[str]:
        """Extract predicted trends"""
        return [line.strip() for line in text.split('\n') 
                if any(word in line.lower() for word in ['trend', 'popular', 'emerging'])][:5]
    
    def _extract_niches(self, text: str) -> List[str]:
        """Extract niche opportunities"""
        return [line.strip() for line in text.split('\n') 
                if 'niche' in line.lower()][:5]


# Initialize analyzer
ai_analyzer = OpenAIAnalyzer()
