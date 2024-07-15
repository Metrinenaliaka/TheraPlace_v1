"""
This file contains the serializers for the client app
"""
from rest_framework import serializers
from .models import ClientUser, ClientProfile, TherapistProfile

class LoginSerializer(serializers.Serializer):
    """
    This class is a serializer for the login endpoint
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class DeleteProfileSerializer(serializers.Serializer):
    """
    This class is a serializer for the delete profile endpoint
    """
    pass

class ClientUserSerializer(serializers.ModelSerializer):
    """
    This class is a serializer for the client user model
    """
    class Meta:
        """
        This class defines the fields that are to be serialized
        """
        model = ClientUser
        fields = ['id', 'username', 'email', 'password', 'role',]

    def create(self, validated_data):
        """
        This function creates a new user
        """
        user = ClientUser.objects.create_user(**validated_data)
        return user

class ClientProfileSerializer(serializers.ModelSerializer):
    """
    This class is a serializer for the client profile model
    """
    user = ClientUserSerializer(source='client', read_only=True)

    def update(self, instance, validated_data):
        """
        This function updates the client profile
        """
        instance.age = validated_data.get('age', instance.age)
        instance.description = validated_data.get('description', instance.description)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.save()
        return instance
    class Meta:
        """
        This class defines the fields that are to be serialized
        """
        model = ClientProfile
        fields = ['age', 'description', 'condition', 'user']

class TherapistProfileSerializer(serializers.ModelSerializer):
    """
    This class is a serializer for the therapist profile model
    """
    user = ClientUserSerializer(source='therapist', read_only=True)
   
    def update(self, instance, validated_data):
        """
        This function updates the therapist profile
        """
        instance.experience = validated_data.get('experience', instance.experience)
        instance.description = validated_data.get('description', instance.description)
        instance.occupation = validated_data.get('occupation', instance.occupation)
        instance.price = validated_data.get('price', instance.price)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance    
    class Meta:
        """
        This class defines the fields that are to be serialized
        """
        model = TherapistProfile
        fields = ['experience', 'description', 'occupation', 'price', 'location', 'user'] 


