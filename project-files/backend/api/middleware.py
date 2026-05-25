"""Custom middleware for security headers, logging, and API key authentication"""

import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework import status
import json

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to all responses"""
    
    def process_response(self, request, response):
        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS filter
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Strict Transport Security (HSTS) - only in production
        if not request.META.get('HTTP_HOST', '').startswith('localhost'):
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response


class RequestLoggingMiddleware(MiddlewareMixin):
    """Log all API requests and responses"""
    
    def process_request(self, request):
        # Store start time
        import time
        request._start_time = time.time()
        
        # Log request
        if request.path.startswith('/api/'):
            logger.info(
                f"API Request: {request.method} {request.path}",
                extra={
                    'method': request.method,
                    'path': request.path,
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'ip': self._get_client_ip(request),
                }
            )
    
    def process_response(self, request, response):
        # Log response time
        if request.path.startswith('/api/') and hasattr(request, '_start_time'):
            import time
            duration = time.time() - request._start_time
            
            logger.info(
                f"API Response: {request.method} {request.path} - {response.status_code} ({duration:.2f}s)",
                extra={
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                    'duration': duration,
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                }
            )
            
            # Log errors
            if response.status_code >= 400:
                logger.error(
                    f"API Error: {request.method} {request.path} - {response.status_code}",
                    extra={
                        'method': request.method,
                        'path': request.path,
                        'status_code': response.status_code,
                        'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    }
                )
        
        return response
    
    @staticmethod
    def _get_client_ip(request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class APIKeyAuthenticationMiddleware(MiddlewareMixin):
    """Authenticate API requests using API key"""
    
    def process_request(self, request):
        # Only process API requests
        if not request.path.startswith('/api/'):
            return None
        
        # Skip if user already authenticated
        if request.user.is_authenticated:
            return None
        
        # Check for API key in header
        api_key = request.META.get('HTTP_X_API_KEY') or \
                  request.META.get('HTTP_AUTHORIZATION', '').replace('ApiKey ', '')
        
        if not api_key:
            return None
        
        # Validate API key
        from api.models import APIKey
        from django.utils import timezone
        
        try:
            key_obj = APIKey.objects.select_related('user').get(
                key=api_key,
                is_active=True
            )
            
            # Update last used timestamp
            key_obj.last_used = timezone.now()
            key_obj.save(update_fields=['last_used'])
            
            # Set request user
            request.user = key_obj.user
            logger.info(f"API Key authenticated: {key_obj.user.username}")
            
        except APIKey.DoesNotExist:
            logger.warning(f"Invalid or inactive API key attempt: {api_key[:10]}...")
            return JsonResponse(
                {'error': 'Invalid API key'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        return None
