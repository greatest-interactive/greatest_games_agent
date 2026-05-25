"""
AI Analysis Engine for Greatest Game Agent.
Uses OpenAI to generate market insights and strategies.
"""
from typing import Dict, List, Any
import openai
from django.conf import settings


class AIAnalysisEngine:
    """Engine for AI-powered analysis using OpenAI."""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-4"
    
    def analyze_market_trends(self, game_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market trends using AI.
        
        Args:
            game_data: Game-related data
            market_data: Market data from Bright Data
            
        Returns:
            Analysis insights
        """
        prompt = f"""
        Analyze the gaming market with the following data:
        
        Game Concept: {game_data.get('concept', 'Unknown')}
        Genre: {game_data.get('genre', 'Unknown')}
        Market Data: {market_data}
        
        Provide:
        1. Trending mechanics in this genre
        2. Rising genres and subgenres
        3. Market gaps and opportunities
        4. Monetization opportunities
        5. Competitive landscape analysis
        
        Format response as JSON with these keys:
        - trending_mechanics (list)
        - rising_genres (list)
        - market_gaps (list)
        - monetization_opportunities (list)
        - competitive_analysis (string)
        - confidence_score (0-100)
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a gaming market analyst AI."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            import json
            analysis_text = response.choices[0].message.content
            # Parse JSON from response
            analysis = json.loads(analysis_text)
            return analysis
        except Exception as e:
            return {
                "error": str(e),
                "trending_mechanics": [],
                "rising_genres": [],
                "market_gaps": [],
                "monetization_opportunities": []
            }
    
    def generate_sentiment_summary(self, sentiment_data: List[Dict[str, Any]]) -> str:
        """
        Generate a summary of player sentiment.
        
        Args:
            sentiment_data: List of sentiment records
            
        Returns:
            Sentiment summary text
        """
        if not sentiment_data:
            return "No sentiment data available."
        
        prompt = f"""
        Summarize player sentiment for a game based on this data:
        
        {sentiment_data}
        
        Provide:
        1. Overall sentiment score
        2. Key pain points
        3. Frequently requested features
        4. Player preferences
        5. Recommendations for improvement
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a player sentiment analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def generate_launch_strategy(self, game_concept: str, genre: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a launch strategy for a game.
        
        Args:
            game_concept: Game concept/name
            genre: Game genre
            market_data: Market data from research
            
        Returns:
            Launch strategy details
        """
        prompt = f"""
        Generate a launch strategy for:
        
        Game: {game_concept}
        Genre: {genre}
        Market Analysis: {market_data}
        
        Provide:
        1. Launch recommendations (list)
        2. Suggested pricing (number)
        3. Market positioning (string)
        4. Best release timing (string)
        5. Viral marketing suggestions (list)
        6. Competing games to analyze (list)
        7. Key differentiation factors (list)
        8. Risk factors and mitigation (list)
        9. Confidence score (0-100)
        
        Format as JSON with these exact keys:
        - launch_recommendations
        - suggested_pricing
        - market_positioning
        - best_release_timing
        - viral_marketing_suggestions
        - competing_games
        - differentiation_factors
        - risk_factors
        - confidence_score
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a game publishing strategy expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2500
            )
            
            import json
            strategy_text = response.choices[0].message.content
            strategy = json.loads(strategy_text)
            return strategy
        except Exception as e:
            return {
                "error": str(e),
                "launch_recommendations": [],
                "suggested_pricing": 19.99,
                "market_positioning": "Indie title with unique mechanics",
                "best_release_timing": "Q2 2026",
                "viral_marketing_suggestions": [],
                "competing_games": [],
                "differentiation_factors": [],
                "risk_factors": [],
                "confidence_score": 0
            }


# Convenience functions
def analyze_market_trends(game_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function for market analysis."""
    engine = AIAnalysisEngine()
    return engine.analyze_market_trends(game_data, market_data)


def generate_sentiment_summary(sentiment_data: List[Dict[str, Any]]) -> str:
    """Convenience function for sentiment summary."""
    engine = AIAnalysisEngine()
    return engine.generate_sentiment_summary(sentiment_data)


def generate_launch_strategy(game_concept: str, genre: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function for launch strategy generation."""
    engine = AIAnalysisEngine()
    return engine.generate_launch_strategy(game_concept, genre, market_data)
