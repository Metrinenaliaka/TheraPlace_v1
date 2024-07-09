"""
Serializers for the app
"""
from rest_framework import serializers
from .models import Client, Therapist

class ClientSerializer(serializers.ModelSerializer):
    """
    serializer for the client model
    """
    class Meta:
        """
        metadata for the model
        """
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'category', 'description', 'condition', 'age']

class TherapistSerializer(serializers.ModelSerializer):
    """
    serializer for the therapist model
    """
    class Meta:
        """
        metadata for the model
        """
        model = Therapist
        fields = ['id', 'name', 'email', 'phone', 'category', 'description', 'client', 'experience', 'price', 'qualification', 'location']


class ClientSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True}
        }

    def create(self, validated_data):
        client = Client.objects.create(**validated_data)
        return client

class TherapistSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Therapist
        fields = '__all__'
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True}
        }

    def create(self, validated_data):
        therapist = Therapist.objects.create(**validated_data)
        return therapist