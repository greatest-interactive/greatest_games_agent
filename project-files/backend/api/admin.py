from django.contrib import admin
from .models import (
    Game, Competitor, Trend, MarketAnalysis, 
    PlayerSentiment, LaunchStrategy
)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'release_date', 'created_at')
    search_fields = ('title', 'developer')
    list_filter = ('platform', 'genre', 'release_date')

@admin.register(Competitor)
class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('game_title', 'platform', 'price', 'updated_at')
    search_fields = ('game_title', 'developer')
    list_filter = ('platform', 'updated_at')

@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'momentum_score', 'created_at')
    search_fields = ('title', 'keywords')
    list_filter = ('category', 'created_at')

@admin.register(MarketAnalysis)
class MarketAnalysisAdmin(admin.ModelAdmin):
    list_display = ('query', 'created_at', 'updated_at')
    search_fields = ('query',)
    list_filter = ('created_at',)

@admin.register(PlayerSentiment)
class PlayerSentimentAdmin(admin.ModelAdmin):
    list_display = ('game_title', 'sentiment_type', 'source', 'created_at')
    search_fields = ('game_title', 'source')
    list_filter = ('sentiment_type', 'source')

@admin.register(LaunchStrategy)
class LaunchStrategyAdmin(admin.ModelAdmin):
    list_display = ('game_concept', 'created_at')
    search_fields = ('game_concept',)
    list_filter = ('created_at',)
