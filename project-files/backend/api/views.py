from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.db.models import Q
from .models import (
    Game, Competitor, Trend, MarketAnalysis, 
    PlayerSentiment, LaunchStrategy, ScrapingJob, ScrapedGame,
    Tier, UserSubscription, TokenUsage
)
from .serializers import (
    GameSerializer, CompetitorSerializer, TrendSerializer,
    MarketAnalysisSerializer, PlayerSentimentSerializer,
    LaunchStrategySerializer, ScrapingJobSerializer, ScrapedGameSerializer,
    TierSerializer, UserSubscriptionSerializer, TokenUsageSerializer
)


class GameViewSet(viewsets.ModelViewSet):
    """API endpoint for managing games."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Game.objects.all()
        platform = self.request.query_params.get('platform')
        genre = self.request.query_params.get('genre')
        search = self.request.query_params.get('search')
        
        if platform:
            queryset = queryset.filter(platform=platform)
        if genre:
            queryset = queryset.filter(genre__contains=[genre])
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(developer__icontains=search)
            )
        return queryset


class CompetitorViewSet(viewsets.ModelViewSet):
    """API endpoint for managing competitor data."""
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Competitor.objects.all()
        platform = self.request.query_params.get('platform')
        genre = self.request.query_params.get('genre')
        
        if platform:
            queryset = queryset.filter(platform=platform)
        if genre:
            queryset = queryset.filter(genre=genre)
        return queryset
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get competitors with recent engagement spikes."""
        competitors = Competitor.objects.filter(
            engagement_spike=True
        ).order_by('-updated_at')[:20]
        serializer = self.get_serializer(competitors, many=True)
        return Response(serializer.data)


class TrendViewSet(viewsets.ModelViewSet):
    """API endpoint for managing trends."""
    queryset = Trend.objects.all()
    serializer_class = TrendSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Trend.objects.all()
        category = self.request.query_params.get('category')
        opportunity_level = self.request.query_params.get('opportunity_level')
        
        if category:
            queryset = queryset.filter(category=category)
        if opportunity_level:
            queryset = queryset.filter(opportunity_level=opportunity_level)
        return queryset.order_by('-momentum_score')


class MarketAnalysisViewSet(viewsets.ModelViewSet):
    """API endpoint for market analysis reports."""
    queryset = MarketAnalysis.objects.all()
    serializer_class = MarketAnalysisSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = MarketAnalysis.objects.all()
        analysis_type = self.request.query_params.get('analysis_type')
        
        if analysis_type:
            queryset = queryset.filter(analysis_type=analysis_type)
        return queryset.order_by('-created_at')


class PlayerSentimentViewSet(viewsets.ModelViewSet):
    """API endpoint for player sentiment data."""
    queryset = PlayerSentiment.objects.all()
    serializer_class = PlayerSentimentSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = PlayerSentiment.objects.all()
        game_title = self.request.query_params.get('game_title')
        source = self.request.query_params.get('source')
        sentiment_type = self.request.query_params.get('sentiment_type')
        
        if game_title:
            queryset = queryset.filter(game_title__icontains=game_title)
        if source:
            queryset = queryset.filter(source=source)
        if sentiment_type:
            queryset = queryset.filter(sentiment_type=sentiment_type)
        return queryset.order_by('-created_at')


class LaunchStrategyViewSet(viewsets.ModelViewSet):
    """API endpoint for launch strategies."""
    queryset = LaunchStrategy.objects.all()
    serializer_class = LaunchStrategySerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate a new launch strategy."""
        from scraper.bright_data_integration import fetch_market_data
        from ai_analysis.analysis_engine import generate_launch_strategy
        
        game_concept = request.data.get('game_concept')
        genre = request.data.get('genre')
        
        try:
            # Fetch market data
            market_data = fetch_market_data(game_concept, genre)
            
            # Generate strategy
            strategy_data = generate_launch_strategy(
                game_concept, genre, market_data
            )
            
            # Save strategy
            strategy = LaunchStrategy.objects.create(
                game_concept=game_concept,
                genre=genre,
                **strategy_data
            )
            
            serializer = self.get_serializer(strategy)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ScrapingJobViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for Bright Data scraping jobs."""
    queryset = ScrapingJob.objects.all()
    serializer_class = ScrapingJobSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = ScrapingJob.objects.all()
        source = self.request.query_params.get('source')
        status_filter = self.request.query_params.get('status')
        
        if source:
            queryset = queryset.filter(source=source)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get games from a specific scraping job."""
        job = self.get_object()
        games = job.games.all()
        serializer = ScrapedGameSerializer(games, many=True)
        return Response({
            'job_id': job.job_id,
            'source': job.source,
            'status': job.status,
            'total_games': games.count(),
            'games': serializer.data
        })


class ScrapedGameViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for scraped games."""
    queryset = ScrapedGame.objects.all()
    serializer_class = ScrapedGameSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = ScrapedGame.objects.all()
        platform = self.request.query_params.get('platform')
        min_rating = self.request.query_params.get('min_rating')
        min_trending = self.request.query_params.get('min_trending')
        
        if platform:
            queryset = queryset.filter(platform=platform)
        if min_rating:
            try:
                queryset = queryset.filter(rating__gte=float(min_rating))
            except (ValueError, TypeError):
                pass
        if min_trending:
            try:
                queryset = queryset.filter(rating__gte=float(min_trending))
            except (ValueError, TypeError):
                pass
        return queryset.order_by('-rating', '-created_at')
    
    @action(detail=False, methods=['get'])
    def by_platform(self, request):
        """Get games grouped by platform."""
        from django.db.models import Count
        
        platform_stats = ScrapedGame.objects.values('platform').annotate(
            count=Count('id'),
            avg_rating=Count('rating')
        )
        
        return Response({
            'by_platform': list(platform_stats)
        })
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending games from recent scrapes."""
        games = self.get_queryset().filter(
            rating__gte=70.0
        )[:50]
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)


# AI Analysis Endpoints
from rest_framework.views import APIView
from api.services.openai_service import ai_analyzer


class TrendAnalysisView(APIView):
    """Analyze gaming trends using AI"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            game_concept = request.data.get('game_concept')
            
            # Get recent trends
            trends = Trend.objects.all().order_by('-momentum_score')[:20]
            trends_data = TrendSerializer(trends, many=True).data
            
            # Get AI analysis
            analysis = ai_analyzer.analyze_trends(trends_data, game_concept)
            
            return Response(analysis)
        except Exception as e:
            return Response(
                {"error": str(e), "status": "failed"},
                status=status.HTTP_400_BAD_REQUEST
            )


class CompetitorAnalysisView(APIView):
    """Analyze competitors using AI"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            game_genre = request.data.get('genre')
            
            # Get competitor data
            competitors = Competitor.objects.all()
            if game_genre:
                competitors = competitors.filter(genre__icontains=game_genre)
            competitors = competitors.order_by('-rating')[:20]
            
            competitors_data = CompetitorSerializer(competitors, many=True).data
            
            # Get AI analysis
            analysis = ai_analyzer.analyze_competitors(competitors_data, game_genre)
            
            return Response(analysis)
        except Exception as e:
            return Response(
                {"error": str(e), "status": "failed"},
                status=status.HTTP_400_BAD_REQUEST
            )


class MarketGapView(APIView):
    """Identify market gaps using AI"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            # Get trends and competitors
            trends = Trend.objects.all().order_by('-momentum_score')[:15]
            competitors = Competitor.objects.all().order_by('-rating')[:15]
            
            trends_data = TrendSerializer(trends, many=True).data
            competitors_data = CompetitorSerializer(competitors, many=True).data
            
            # Get AI analysis
            analysis = ai_analyzer.identify_market_gaps(trends_data, competitors_data)
            
            return Response(analysis)
        except Exception as e:
            return Response(
                {"error": str(e), "status": "failed"},
                status=status.HTTP_400_BAD_REQUEST
            )


class LaunchStrategyGeneratorView(APIView):
    """Generate launch strategy using AI"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            game_concept = request.data.get('game_concept')
            genre = request.data.get('genre')
            target_audience = request.data.get('target_audience')
            
            if not all([game_concept, genre, target_audience]):
                return Response(
                    {"error": "Missing required fields: game_concept, genre, target_audience"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get trends for context
            trends = Trend.objects.all().order_by('-momentum_score')[:10]
            trends_data = TrendSerializer(trends, many=True).data
            
            # Generate strategy
            strategy = ai_analyzer.generate_launch_strategy(
                game_concept, 
                genre, 
                target_audience,
                trends_data
            )
            
            # Save to database
            if strategy.get('status') == 'success':
                LaunchStrategy.objects.create(
                    game_concept=game_concept,
                    genre=genre,
                    target_audience=target_audience,
                    launch_recommendations=strategy.get('launch_recommendations', []),
                    market_positioning=strategy.get('strategy', ''),
                    best_release_timing=strategy.get('best_release_window', ''),
                    viral_marketing_suggestions=strategy.get('marketing_channels', []),
                    confidence_score=strategy.get('confidence_score', 0)
                )
            
            return Response(strategy)
        except Exception as e:
            return Response(
                {"error": str(e), "status": "failed"},
                status=status.HTTP_400_BAD_REQUEST
            )


class TrendPredictionView(APIView):
    """Predict upcoming trends using AI"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            timeframe = request.data.get('timeframe', '6 months')
            
            # Get historical trends
            trends = Trend.objects.all().order_by('-momentum_score')[:20]
            trends_data = TrendSerializer(trends, many=True).data
            
            # Generate predictions
            predictions = ai_analyzer.predict_trends(trends_data, timeframe)
            
            return Response(predictions)
        except Exception as e:
            return Response(
                {"error": str(e), "status": "failed"},
                status=status.HTTP_400_BAD_REQUEST
            )


class AIAgentQueryView(APIView):
    """General AI agent for custom queries"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            query = request.data.get('query')
            include_context = request.data.get('include_context', True)
            
            if not query:
                return Response(
                    {"error": "Query is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get context data if requested
            context_data = None
            if include_context:
                trends = Trend.objects.all().order_by('-momentum_score')[:5]
                competitors = Competitor.objects.all().order_by('-rating')[:5]
                
                context_data = {
                    'trends': TrendSerializer(trends, many=True).data,
                    'competitors': CompetitorSerializer(competitors, many=True).data
                }
            
            # Get AI response
            response = ai_analyzer.query_ai_agent(query, context_data)
            
            return Response(response)
        except Exception as e:
            return Response(
                {"error": str(e), "status": "failed"},
                status=status.HTTP_400_BAD_REQUEST
            )


# Tier System Views
class TierViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for subscription tiers"""
    queryset = Tier.objects.filter(is_active=True)
    serializer_class = TierSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def compare(self, request):
        """Get all tiers for comparison"""
        tiers = self.get_queryset().order_by('price_monthly')
        serializer = self.get_serializer(tiers, many=True)
        return Response({
            'tiers': serializer.data,
            'currency': 'USD',
            'billing_period': 'monthly'
        })


class UserSubscriptionView(APIView):
    """Get current user's subscription"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            subscription = UserSubscription.objects.get(user=request.user)
            serializer = UserSubscriptionSerializer(subscription)
            return Response(serializer.data)
        except UserSubscription.DoesNotExist:
            # Create free tier subscription if doesn't exist
            free_tier = Tier.objects.get(name='free')
            subscription = UserSubscription.objects.create(
                user=request.user,
                tier=free_tier,
                payment_method='free'
            )
            serializer = UserSubscriptionSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class TokenUsageView(APIView):
    """Track and retrieve token usage"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get current user's token usage"""
        try:
            subscription = UserSubscription.objects.get(user=request.user)
            usage_history = TokenUsage.objects.filter(user=request.user).order_by('-created_at')[:20]
            
            serializer = TokenUsageSerializer(usage_history, many=True)
            return Response({
                'subscription': UserSubscriptionSerializer(subscription).data,
                'recent_usage': serializer.data
            })
        except UserSubscription.DoesNotExist:
            return Response(
                {"error": "User subscription not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def post(self, request):
        """Record token usage (internal use)"""
        try:
            action_type = request.data.get('action_type')
            tokens_spent = request.data.get('tokens_spent', 0)
            description = request.data.get('description', '')
            
            # Record usage
            TokenUsage.objects.create(
                user=request.user,
                action_type=action_type,
                tokens_spent=tokens_spent,
                description=description
            )
            
            # Update subscription usage
            subscription = UserSubscription.objects.get(user=request.user)
            subscription.tokens_used_this_month += tokens_spent
            subscription.save()
            
            return Response({
                'tokens_spent': tokens_spent,
                'tokens_remaining': subscription.tokens_remaining()
            })
        except UserSubscription.DoesNotExist:
            return Response(
                {"error": "User subscription not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
