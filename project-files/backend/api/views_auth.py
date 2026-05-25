"""Authentication views for user registration, login, and token management"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
import logging

from .models import APIKey, UserProfile
from .serializers_auth import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    APIKeySerializer,
    APIKeyCreateSerializer
)

logger = logging.getLogger(__name__)


class UserRegistrationView(APIView):
    """User registration endpoint"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'User created successfully. API key has been generated.'
            }, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login endpoint"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            if user is None:
                logger.warning(f"Login failed for user: {username}")
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            logger.info(f"User logged in: {username}")
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """Get current user details"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Update user profile"""
        user = request.user
        
        # Update user fields
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'email' in request.data:
            user.email = request.data['email']
        
        user.save()
        
        # Update profile fields
        if 'company' in request.data or 'role' in request.data:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            if 'company' in request.data:
                profile.company = request.data['company']
            if 'role' in request.data and request.user.profile.role == 'admin':
                profile.role = request.data['role']
            profile.save()
        
        logger.info(f"User updated: {user.username}")
        return Response(UserSerializer(user).data)


class ChangePasswordView(APIView):
    """Change user password"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response(
                {'error': 'Old password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        # Generate new tokens
        refresh = RefreshToken.for_user(user)
        
        logger.info(f"Password changed for user: {user.username}")
        return Response({
            'message': 'Password changed successfully',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class APIKeyViewSet(viewsets.ViewSet):
    """API Key management"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List all API keys for current user"""
        api_keys = APIKey.objects.filter(user=request.user)
        serializer = APIKeySerializer(api_keys, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Create a new API key"""
        serializer = APIKeyCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            api_key = serializer.save()
            return Response(
                {
                    'id': api_key.id,
                    'name': api_key.name,
                    'key': api_key.key,  # Show full key only once
                    'created_at': api_key.created_at,
                    'message': 'API key created. Store it safely - it won\'t be shown again.'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """Revoke/delete an API key"""
        try:
            api_key = APIKey.objects.get(id=pk, user=request.user)
            api_key.delete()
            logger.info(f"API key deleted for user: {request.user.username}")
            return Response(
                {'message': 'API key revoked'},
                status=status.HTTP_204_NO_CONTENT
            )
        except APIKey.DoesNotExist:
            return Response(
                {'error': 'API key not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None):
        """Revoke an API key"""
        try:
            api_key = APIKey.objects.get(id=pk, user=request.user)
            api_key.is_active = False
            api_key.save()
            logger.info(f"API key deactivated for user: {request.user.username}")
            return Response({'message': 'API key revoked'})
        except APIKey.DoesNotExist:
            return Response(
                {'error': 'API key not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def validate(self, request):
        """Validate an API key (unauthenticated endpoint)"""
        api_key = request.data.get('key')
        if not api_key:
            return Response(
                {'error': 'API key required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            key_obj = APIKey.objects.get(key=api_key, is_active=True)
            key_obj.last_used = timezone.now()
            key_obj.save()
            return Response({'valid': True, 'user': key_obj.user.username})
        except APIKey.DoesNotExist:
            return Response(
                {'valid': False, 'error': 'Invalid API key'},
                status=status.HTTP_401_UNAUTHORIZED
            )
