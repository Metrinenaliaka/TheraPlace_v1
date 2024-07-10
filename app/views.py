"""
my viewsets for the app
"""
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.mixins import CreateModelMixin
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile, ClientProfile, TherapistProfile
from .serializers import ProfileSerializer, ClientProfileSerializer, TherapistProfileSerializer


class SignupViewSet(viewsets.GenericViewSet, CreateModelMixin):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]


class LoginViewSet(viewsets.ViewSet):
    """
    A viewset for handling user authentication (login).
    """
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        if profile.category == 'client':
            return TherapistProfile.objects.all()
        elif profile.category == 'therapist':
            return ClientProfile.objects.all()
        return []

    def get_serializer_class(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        if profile.category == 'client':
            return TherapistProfileSerializer
        elif profile.category == 'therapist':
            return ClientProfileSerializer
        return None

    # @action(detail=False, methods=['get'])
    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()

        if serializer_class is None:
            return Response({'error': 'Profile not found or invalid user role'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        user = request.user
        profile = Profile.objects.get(user=user)

        if profile.category == 'client':
            instance = ClientProfile.objects.get(user=user)
            serializer = ClientProfileSerializer(instance, data=request.data)
        elif profile.category == 'therapist':
            instance = TherapistProfile.objects.get(user=user)
            serializer = TherapistProfileSerializer(instance, data=request.data)
        else:
            return Response({'error': 'Invalid user role'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)