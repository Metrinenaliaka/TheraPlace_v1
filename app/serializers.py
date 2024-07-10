"""
Serializers for the app
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ClientProfile, TherapistProfile

class UserSerializer(serializers.ModelSerializer):
    # Serializer for the User model to control which fields are included in the API response
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer to include user data within profile
    

    class Meta:
        model = Profile
        fields = ['user', 'category']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            profile = Profile.objects.create(user=user, **validated_data)
            return profile
        return user_serializer.errors

class ClientProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()  # Nested serializer to include profile data within client profile

    class Meta:
        model = ClientProfile
        fields = '__all__'

class TherapistProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()  # Nested serializer to include profile data within therapist profile

    class Meta:
        model = TherapistProfile
        fields = '__all__'

