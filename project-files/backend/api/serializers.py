from rest_framework import serializers
from .models import (
    Game, Competitor, Trend, MarketAnalysis, 
    PlayerSentiment, LaunchStrategy, ScrapingJob, ScrapedGame,
    Tier, UserSubscription, TokenUsage, Payment, Invoice, AnalyticsEvent, TierChange
)


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'id', 'title', 'developer', 'genre', 'tags', 'description',
            'price', 'rating', 'review_count', 'platform', 'url',
            'release_date', 'created_at', 'updated_at'
        ]


class CompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        fields = [
            'id', 'game_title', 'developer', 'platform', 'genre',
            'price', 'rating', 'review_count', 'downloads',
            'price_change', 'engagement_spike', 'social_mentions',
            'sentiment_overview', 'url', 'created_at', 'updated_at'
        ]


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = [
            'id', 'title', 'category', 'description', 'keywords',
            'momentum_score', 'growth_rate', 'search_volume',
            'market_gap', 'opportunity_level', 'supporting_data',
            'created_at', 'updated_at'
        ]


class MarketAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketAnalysis
        fields = [
            'id', 'query', 'analysis_type', 'ai_insights',
            'trending_mechanics', 'rising_genres', 'market_gaps',
            'monetization_opportunities', 'confidence_score',
            'created_at', 'updated_at'
        ]


class PlayerSentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerSentiment
        fields = [
            'id', 'game_title', 'sentiment_type', 'source',
            'sentiment_score', 'comment', 'key_themes',
            'engagement_metric', 'url', 'created_at'
        ]


class LaunchStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = LaunchStrategy
        fields = [
            'id', 'game_concept', 'genre', 'target_audience',
            'launch_recommendations', 'suggested_pricing',
            'market_positioning', 'best_release_timing',
            'viral_marketing_suggestions', 'competing_games',
            'differentiation_factors', 'risk_factors',
            'confidence_score', 'created_at', 'updated_at'
        ]


class ScrapingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapingJob
        fields = [
            'id', 'job_id', 'source', 'query', 'status',
            'results_count', 'error_message', 'created_at',
            'updated_at', 'completed_at'
        ]


class ScrapedGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedGame
        fields = [
            'id', 'platform', 'title', 'developer', 'url',
            'price', 'rating', 'review_count', 'tags', 'raw_data',
            'created_at', 'updated_at'
        ]


# Tier System Serializers
class TierSerializer(serializers.ModelSerializer):
    """Serializer for subscription tiers"""
    class Meta:
        model = Tier
        fields = [
            'id', 'name', 'display_name', 'description', 'price_monthly',
            'price_yearly', 'monthly_tokens', 'max_saved_games',
            'max_api_requests_per_day', 'max_scraping_jobs', 'features',
            'is_active', 'created_at'
        ]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for user subscriptions"""
    tier_name = serializers.CharField(source='tier.display_name', read_only=True)
    tokens_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSubscription
        fields = [
            'id', 'tier', 'tier_name', 'tokens_used_this_month', 'tokens_remaining',
            'is_active', 'payment_method', 'started_at', 'expires_at', 'renewal_date'
        ]
        read_only_fields = ['id', 'tokens_remaining', 'started_at']
    
    def get_tokens_remaining(self, obj):
        """Get remaining tokens for user's subscription"""
        return obj.tokens_remaining()


class TokenUsageSerializer(serializers.ModelSerializer):
    """Serializer for token usage records"""
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    
    class Meta:
        model = TokenUsage
        fields = ['id', 'action_type', 'action_type_display', 'tokens_spent', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payment transactions"""
    tier_name = serializers.CharField(source='tier.display_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'stripe_charge_id', 'amount', 'currency', 'tier', 'tier_name',
            'billing_period', 'status', 'description', 'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'completed_at']


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for invoices"""
    tier_name = serializers.CharField(source='tier.display_name', read_only=True)
    payment = PaymentSerializer(read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'tier', 'tier_name', 'amount', 'currency',
            'billing_period_start', 'billing_period_end', 'status',
            'due_date', 'pdf_url', 'payment', 'created_at'
        ]
        read_only_fields = ['id', 'invoice_number', 'created_at']


class AnalyticsEventSerializer(serializers.ModelSerializer):
    """Serializer for analytics events"""
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    
    class Meta:
        model = AnalyticsEvent
        fields = [
            'id', 'event_type', 'event_type_display', 'event_name', 'page',
            'metadata', 'duration_seconds', 'session_id', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        fields = [
            'id', 'tier', 'tier_name', 'started_at', 'expires_at',
            'renewal_date', 'tokens_used_this_month', 'tokens_remaining',
            'is_active', 'payment_method', 'created_at'
        ]
        read_only_fields = ['tokens_used_this_month', 'tokens_reset_at']
    
    def get_tokens_remaining(self, obj):
        return obj.tokens_remaining()


class TokenUsageSerializer(serializers.ModelSerializer):
    """Serializer for tracking token usage"""
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    
    class Meta:
        model = TokenUsage
        fields = [
            'id', 'action_type', 'action_type_display', 'tokens_spent',
            'description', 'created_at'
        ]
        read_only_fields = ['created_at']


class TierChangeSerializer(serializers.ModelSerializer):
    """Serializer for tier change tracking"""
    from_tier_name = serializers.CharField(source='from_tier.display_name', read_only=True)
    to_tier_name = serializers.CharField(source='to_tier.display_name', read_only=True)
    
    class Meta:
        model = TierChange
        fields = [
            'id', 'user', 'from_tier', 'from_tier_name', 'to_tier', 'to_tier_name',
            'change_type', 'payment', 'billing_period', 'amount_charged',
            'prorated_credit', 'effective_date', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'prorated_credit']
