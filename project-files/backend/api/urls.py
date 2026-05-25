from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from . import views_auth
from . import views_payment

router = DefaultRouter()
router.register(r'games', views.GameViewSet)
router.register(r'competitors', views.CompetitorViewSet)
router.register(r'trends', views.TrendViewSet)
router.register(r'analysis', views.MarketAnalysisViewSet)
router.register(r'sentiment', views.PlayerSentimentViewSet)
router.register(r'strategies', views.LaunchStrategyViewSet)
router.register(r'scraping-jobs', views.ScrapingJobViewSet, basename='scraping-job')
router.register(r'scraped-games', views.ScrapedGameViewSet, basename='scraped-game')
router.register(r'api-keys', views_auth.APIKeyViewSet, basename='api-key')
router.register(r'tiers', views.TierViewSet, basename='tier')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    
    # Authentication Endpoints
    path('auth/register/', views_auth.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views_auth.UserLoginView.as_view(), name='login'),
    path('auth/me/', views_auth.UserDetailView.as_view(), name='user-detail'),
    path('auth/change-password/', views_auth.ChangePasswordView.as_view(), name='change-password'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # AI Analysis Endpoints
    path('ai/analyze-trends/', views.TrendAnalysisView.as_view(), name='analyze-trends'),
    path('ai/analyze-competitors/', views.CompetitorAnalysisView.as_view(), name='analyze-competitors'),
    path('ai/market-gaps/', views.MarketGapView.as_view(), name='market-gaps'),
    path('ai/generate-strategy/', views.LaunchStrategyGeneratorView.as_view(), name='generate-strategy'),
    path('ai/predict-trends/', views.TrendPredictionView.as_view(), name='predict-trends'),
    path('ai/query/', views.AIAgentQueryView.as_view(), name='ai-query'),
    
    # Subscription & Billing Endpoints
    path('subscription/', views.UserSubscriptionView.as_view(), name='user-subscription'),
    path('tokens/', views.TokenUsageView.as_view(), name='token-usage'),
    
    # Payment & Billing Endpoints
    path('payments/intent/', views_payment.PaymentIntentView.as_view(), name='payment-intent'),
    path('payments/confirm/', views_payment.ConfirmPaymentView.as_view(), name='confirm-payment'),
    path('payments/history/', views_payment.PaymentHistoryView.as_view(), name='payment-history'),
    path('invoices/', views_payment.InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/<int:invoice_id>/', views_payment.InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/<int:invoice_id>/pdf/generate/', views_payment.GenerateInvoicePDFView.as_view(), name='generate-invoice-pdf'),
    path('invoices/<int:invoice_id>/pdf/download/', views_payment.DownloadInvoicePDFView.as_view(), name='download-invoice-pdf'),
    
    # Tier Management Endpoints
    path('tiers/available/', views_payment.GetAvailableTiersView.as_view(), name='available-tiers'),
    path('tiers/current/', views_payment.GetCurrentTierView.as_view(), name='current-tier'),
    path('tiers/upgrade/', views_payment.TierUpgradeView.as_view(), name='tier-upgrade'),
    
    # Analytics Endpoints
    path('analytics/events/', views_payment.AnalyticsEventView.as_view(), name='analytics-events'),
    path('analytics/dashboard/', views_payment.AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    
    # Data Export Endpoints
    path('export/payments/', views_payment.ExportPaymentsView.as_view(), name='export-payments'),
    path('export/invoices/', views_payment.ExportInvoicesView.as_view(), name='export-invoices'),
    path('export/analytics/', views_payment.ExportAnalyticsView.as_view(), name='export-analytics'),
    path('export/user-data/', views_payment.ExportUserDataView.as_view(), name='export-user-data'),
    
    # Webhooks
    path('webhooks/stripe/', views_payment.WebhookView.as_view(), name='stripe-webhook'),
    path('webhooks/events/', views_payment.WebhookEventListView.as_view(), name='webhook-events-list'),
    path('webhooks/events/<int:event_id>/', views_payment.WebhookEventDetailView.as_view(), name='webhook-event-detail'),
    path('webhooks/events/<int:event_id>/retry/', views_payment.WebhookEventRetryView.as_view(), name='webhook-event-retry'),
    path('webhooks/stats/', views_payment.WebhookStatsView.as_view(), name='webhook-stats'),
]
