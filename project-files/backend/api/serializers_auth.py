"""Authentication serializers for user registration, login, and API key management"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import APIKey, UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    company = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'company')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        company = validated_data.pop('company', '')
        validated_data.pop('password2')
        
        user = User.objects.create_user(**validated_data)
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            company=company,
            role='user'
        )
        
        # Create API key
        api_key = APIKey.objects.create(
            user=user,
            key=APIKey.generate_key(),
            name='Default API Key'
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data"""
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'profile')
    
    def get_profile(self, obj):
        try:
            profile = obj.profile
            return {
                'company': profile.company,
                'role': profile.get_role_display(),
                'is_verified': profile.is_verified,
                'created_at': profile.created_at,
            }
        except UserProfile.DoesNotExist:
            return None


class APIKeySerializer(serializers.ModelSerializer):
    """Serializer for API key management"""
    user = serializers.StringRelatedField(read_only=True)
    key = serializers.CharField(read_only=True)
    
    class Meta:
        model = APIKey
        fields = ('id', 'user', 'key', 'name', 'is_active', 'created_at', 'last_used')
        read_only_fields = ('created_at', 'last_used')
    
    def create(self, validated_data):
        validated_data['key'] = APIKey.generate_key()
        return super().create(validated_data)


class APIKeyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new API keys - returns full key"""
    
    class Meta:
        model = APIKey
        fields = ('name',)
    
    def create(self, validated_data):
        user = self.context['request'].user
        api_key = APIKey.objects.create(
            user=user,
            key=APIKey.generate_key(),
            **validated_data
        )
        return api_key
