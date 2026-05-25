from django.db import models
from django.contrib.auth.models import User
import secrets


# Authentication & Authorization Models
class APIKey(models.Model):
    """User API key for programmatic access"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_key')
    key = models.CharField(max_length=40, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100, default='Default API Key')
    
    class Meta:
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    @staticmethod
    def generate_key():
        """Generate a unique API key"""
        return secrets.token_urlsafe(32)


class UserProfile(models.Model):
    """Extended user profile for additional fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Administrator'),
        ('analyst', 'Game Analyst'),
        ('developer', 'Game Developer'),
        ('user', 'Basic User'),
    ], default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


# Monetization & Tier System Models
class Tier(models.Model):
    """Subscription tier definitions"""
    TIER_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    
    name = models.CharField(max_length=50, choices=TIER_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField()
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Token Limits (monthly)
    monthly_tokens = models.IntegerField(default=50, help_text="Monthly token allowance")
    
    # Feature Limits
    max_saved_games = models.IntegerField(default=5, help_text="Maximum saved games")
    max_api_requests_per_day = models.IntegerField(default=100)
    max_scraping_jobs = models.IntegerField(default=5, help_text="Max concurrent scraping jobs")
    
    # Features
    features = models.JSONField(default=list, help_text="List of feature names available in this tier")
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['price_monthly']
    
    def __str__(self):
        return self.display_name


class UserSubscription(models.Model):
    """Track user's current subscription"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True)
    
    # Subscription Details
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Null = no expiration (free tier)")
    renewal_date = models.DateField(null=True, blank=True)
    
    # Token Tracking
    tokens_used_this_month = models.IntegerField(default=0)
    tokens_reset_at = models.DateTimeField(auto_now_add=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=50, blank=True, choices=[
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('free', 'Free Tier'),
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Subscription'
        verbose_name_plural = 'User Subscriptions'
    
    def __str__(self):
        return f"{self.user.username} - {self.tier.display_name if self.tier else 'No Tier'}"
    
    def tokens_remaining(self):
        """Calculate remaining tokens for this month"""
        if not self.tier:
            return 0
        return max(0, self.tier.monthly_tokens - self.tokens_used_this_month)


class TokenUsage(models.Model):
    """Track individual token usage for auditing"""
    ACTION_CHOICES = [
        ('scrape', 'Scraping Request'),
        ('api_call', 'API Call'),
        ('analysis', 'AI Analysis'),
        ('export', 'Data Export'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='token_usage')
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    tokens_spent = models.IntegerField()
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action_type']),
        ]
        verbose_name = 'Token Usage'
        verbose_name_plural = 'Token Usage'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_type_display()} ({self.tokens_spent} tokens)"


class Game(models.Model):
    """Model for storing game data from marketplaces."""
    PLATFORM_CHOICES = [
        ('steam', 'Steam'),
        ('epic', 'Epic Games'),
        ('itch', 'itch.io'),
        ('mobile', 'Mobile'),
        ('roblox', 'Roblox'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    developer = models.CharField(max_length=255)
    genre = models.JSONField(default=list)
    tags = models.JSONField(default=list)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    review_count = models.IntegerField(default=0)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField(unique=True)
    release_date = models.DateField(null=True, blank=True)
    scraped_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['platform', '-updated_at']),
            models.Index(fields=['genre']),
        ]
    
    def __str__(self):
        return self.title


class Competitor(models.Model):
    """Model for tracking competitor games and their metrics."""
    game_title = models.CharField(max_length=255)
    developer = models.CharField(max_length=255)
    platform = models.CharField(max_length=20)
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    review_count = models.IntegerField(default=0)
    downloads = models.IntegerField(null=True, blank=True)
    price_change = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    engagement_spike = models.BooleanField(default=False)
    social_mentions = models.IntegerField(default=0)
    sentiment_overview = models.JSONField(default=dict)
    url = models.URLField()
    last_scraped = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['platform', 'genre']),
            models.Index(fields=['-updated_at']),
        ]
    
    def __str__(self):
        return self.game_title


class Trend(models.Model):
    """Model for storing trending topics and mechanics."""
    CATEGORY_CHOICES = [
        ('genre', 'Genre'),
        ('mechanic', 'Mechanic'),
        ('aesthetic', 'Aesthetic'),
        ('platform', 'Platform'),
        ('technology', 'Technology'),
        ('monetization', 'Monetization'),
    ]
    
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    keywords = models.JSONField(default=list)
    momentum_score = models.FloatField(help_text="0-100 scale")
    growth_rate = models.FloatField(default=0, help_text="Percentage growth")
    search_volume = models.IntegerField(default=0)
    market_gap = models.TextField(blank=True)
    opportunity_level = models.CharField(
        max_length=10, 
        choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')],
        default='medium'
    )
    supporting_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-momentum_score']
        indexes = [
            models.Index(fields=['category', '-momentum_score']),
        ]
    
    def __str__(self):
        return self.title


class MarketAnalysis(models.Model):
    """Model for storing AI-generated market analysis reports."""
    query = models.CharField(max_length=500)
    analysis_type = models.CharField(
        max_length=50,
        choices=[
            ('niche_discovery', 'Niche Discovery'),
            ('competitor_analysis', 'Competitor Analysis'),
            ('trend_analysis', 'Trend Analysis'),
            ('market_gap', 'Market Gap'),
        ]
    )
    ai_insights = models.JSONField(default=dict)
    trending_mechanics = models.JSONField(default=list)
    rising_genres = models.JSONField(default=list)
    market_gaps = models.JSONField(default=list)
    monetization_opportunities = models.JSONField(default=list)
    confidence_score = models.FloatField(help_text="0-100 scale")
    raw_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['analysis_type', '-created_at']),
        ]
    
    def __str__(self):
        return f"Analysis: {self.query}"


class PlayerSentiment(models.Model):
    """Model for storing player sentiment data."""
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]
    
    SOURCE_CHOICES = [
        ('reddit', 'Reddit'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('steam', 'Steam'),
        ('twitter', 'Twitter'),
        ('discord', 'Discord'),
    ]
    
    game_title = models.CharField(max_length=255)
    sentiment_type = models.CharField(max_length=20, choices=SENTIMENT_CHOICES)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    sentiment_score = models.FloatField(help_text="-1 to 1 scale")
    comment = models.TextField()
    key_themes = models.JSONField(default=list)
    engagement_metric = models.IntegerField(default=0, help_text="Likes, upvotes, views")
    url = models.URLField(blank=True)
    raw_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['game_title', 'source', '-created_at']),
            models.Index(fields=['sentiment_type']),
        ]
    
    def __str__(self):
        return f"{self.game_title} - {self.sentiment_type}"


class LaunchStrategy(models.Model):
    """Model for storing AI-generated launch strategies."""
    game_concept = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    target_audience = models.CharField(max_length=255)
    launch_recommendations = models.JSONField(default=dict)
    suggested_pricing = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    market_positioning = models.TextField()
    best_release_timing = models.CharField(max_length=255)
    viral_marketing_suggestions = models.JSONField(default=list)
    competing_games = models.JSONField(default=list)
    differentiation_factors = models.JSONField(default=list)
    risk_factors = models.JSONField(default=list)
    confidence_score = models.FloatField(help_text="0-100 scale")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Strategy: {self.game_concept}"


class ScrapingJob(models.Model):
    """Model for tracking Bright Data scraping jobs"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    SOURCE_CHOICES = [
        ('steam', 'Steam'),
        ('itch_io', 'itch.io'),
        ('epic', 'Epic Games Store'),
        ('google_trends', 'Google Trends'),
        ('social_media', 'Social Media'),
    ]
    
    job_id = models.CharField(max_length=255, unique=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    query = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    results_count = models.IntegerField(default=0)
    raw_data = models.JSONField(default=dict)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['source']),
        ]
    
    def __str__(self):
        return f"{self.source.upper()} - {self.query} ({self.status})"


class ScrapedGame(models.Model):
    """Model for games scraped from marketplaces"""
    platform = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    developer = models.CharField(max_length=255, blank=True)
    url = models.URLField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    review_count = models.IntegerField(default=0)
    tags = models.JSONField(default=list)
    raw_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['platform', '-updated_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.platform}"


# Payment & Billing Models
class Payment(models.Model):
    """Track Stripe payment transactions"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    stripe_charge_id = models.CharField(max_length=255, unique=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True)
    
    # Subscription type
    billing_period = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ], default='monthly')
    
    # Payment status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self):
        return f"{self.user.username} - ${self.amount} ({self.status})"


class Invoice(models.Model):
    """Track billing invoices"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    
    invoice_number = models.CharField(max_length=50, unique=True)
    stripe_invoice_id = models.CharField(max_length=255, blank=True)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True)
    
    # Invoice details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    billing_period_start = models.DateField()
    billing_period_end = models.DateField()
    
    # Invoice status
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('paid', 'Paid'),
        ('uncollectible', 'Uncollectible'),
    ], default='sent')
    
    # PDF storage
    pdf_url = models.URLField(blank=True)
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True, help_text="Generated PDF invoice file")
    
    # Timestamps
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.user.username}"


class AnalyticsEvent(models.Model):
    """Detailed tracking of user feature usage for analytics"""
    EVENT_TYPES = [
        ('feature_view', 'Feature Viewed'),
        ('scrape_started', 'Scraping Started'),
        ('scrape_completed', 'Scraping Completed'),
        ('api_call', 'API Call'),
        ('export', 'Data Exported'),
        ('report_generated', 'Report Generated'),
        ('upgrade_clicked', 'Upgrade Clicked'),
        ('page_visited', 'Page Visited'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics_events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_name = models.CharField(max_length=255)
    page = models.CharField(max_length=255, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, help_text="Custom event data")
    duration_seconds = models.FloatField(null=True, blank=True, help_text="How long the action took")
    
    # Session tracking
    session_id = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['event_type']),
        ]
        verbose_name = 'Analytics Event'
        verbose_name_plural = 'Analytics Events'
    
    def __str__(self):
        return f"{self.user.username} - {self.event_type}"


class TierChange(models.Model):
    """Track user subscription tier changes (upgrades/downgrades)"""
    CHANGE_TYPE_CHOICES = [
        ('upgrade', 'Upgrade'),
        ('downgrade', 'Downgrade'),
        ('change', 'Tier Change'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tier_changes')
    from_tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, blank=True, related_name='downgrade_from')
    to_tier = models.ForeignKey(Tier, on_delete=models.CASCADE, related_name='upgrade_to')
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    
    # Payment Info
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='tier_change')
    billing_period = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])
    amount_charged = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Proration Details
    prorated_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Credit from previous tier")
    effective_date = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
        verbose_name = 'Tier Change'
        verbose_name_plural = 'Tier Changes'
    
    def __str__(self):
        return f"{self.user.username}: {self.from_tier} → {self.to_tier}"


class WebhookEvent(models.Model):
    """Log all incoming Stripe webhook events for auditing and debugging"""
    EVENT_STATUS_CHOICES = [
        ('received', 'Received'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('ignored', 'Ignored'),
    ]
    
    # Stripe event details
    stripe_event_id = models.CharField(max_length=255, unique=True, db_index=True, help_text="Stripe event ID")
    event_type = models.CharField(max_length=100, help_text="e.g., payment_intent.succeeded")
    api_version = models.CharField(max_length=20, blank=True)
    
    # Raw event data
    raw_data = models.JSONField(help_text="Full Stripe webhook event payload")
    
    # Processing status
    status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES, default='received')
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Related objects
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='webhook_events')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='webhook_events')
    
    # Error tracking
    error_message = models.TextField(blank=True, help_text="Error message if processing failed")
    retry_count = models.IntegerField(default=0)
    
    # Timestamps
    received_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-received_at']
        indexes = [
            models.Index(fields=['stripe_event_id']),
            models.Index(fields=['event_type']),
            models.Index(fields=['status']),
            models.Index(fields=['user', '-received_at']),
        ]
        verbose_name = 'Webhook Event'
        verbose_name_plural = 'Webhook Events'
    
    def __str__(self):
        return f"{self.event_type} - {self.stripe_event_id}"
