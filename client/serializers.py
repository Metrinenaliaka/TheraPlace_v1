from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import ClientUser, ClientProfile, TherapistProfile

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class ClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = ClientUser.objects.create_user(**validated_data)
        return user

class ClientProfileSerializer(serializers.ModelSerializer):
    # def get_fields(self):
    #     user_role = ClientUser.Role
    #     if user_role == ClientUser.Role.CLIENT:
    #         return ['age', 'description', 'condition']  # Fields for clients
    #     else:
    #         raise AssertionError("Serializer context missing user role")
    def update(self, instance, validated_data):
        instance.age = validated_data.get('age', instance.age)
        instance.description = validated_data.get('description', instance.description)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.save()
        return instance
    class Meta:
        model = ClientProfile
        fields = '__all__'

class TherapistProfileSerializer(serializers.ModelSerializer):
    # def get_fields(self):
    #     user_role = ClientUser.Role
    #     if user_role == ClientUser.Role.CLIENT:
    #         return ['experience', 'description', 'occupation', 'price', 'location']
    #     else:
    #         raise AssertionError("Serializer context missing user role")
    def update(self, instance, validated_data):
        instance.experience = validated_data.get('experience', instance.experience)
        instance.description = validated_data.get('description', instance.description)
        instance.occupation = validated_data.get('occupation', instance.occupation)
        instance.price = validated_data.get('price', instance.price)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance
    
    class Meta:
        model = TherapistProfile
        fields = '__all__'
