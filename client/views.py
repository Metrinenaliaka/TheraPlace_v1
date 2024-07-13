# yourapp/views.py
from django.urls import reverse
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework.exceptions import NotFound
from .models import ClientUser, ClientProfile, TherapistProfile
from .serializers import ClientUserSerializer, ClientProfileSerializer, TherapistProfileSerializer, LoginSerializer

User = get_user_model()

class LoginViewset(viewsets.GenericViewSet):
    """
    Handles login and potentially retrieves user profile data.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        # Use the serializer to validate the input data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Extract validated data
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user:
            # Create or get the token for the user
            token, created = Token.objects.get_or_create(user=user)
            redirect_url = reverse('update-profile')
            return redirect(redirect_url)
            # return Response({'token': token.key})
        else:
            # Return an error response if authentication fails
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SignUpViewset(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ClientUserSerializer

    def post(self, request):
        serializer = ClientUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileViewset(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        
        # Determine which profile serializer to use based on user role
        if user.role == 'CL':  # Assuming 'CL' signifies client role
            serializer_class = ClientProfileSerializer
        elif user.role == 'TH':  # Assuming 'THERA' signifies therapist role
            serializer_class = TherapistProfileSerializer
        else:
            # Handle the case where the user role is undefined or unexpected
            raise AssertionError("User role not recognized")
        return serializer_class
    
    @action(detail=False, methods=['post'])
    def update_profile(self, request):
        serializer_class = self.get_serializer_class()

        # Ensure the user has a profile; create one if it doesn't exist
        user = self.request.user
        if user.role == 'CL':
            profile, created = ClientProfile.objects.get_or_create(client=user)
        elif user.role == 'TH':
            profile, created = TherapistProfile.objects.get_or_create(therapist=user)
        else:
            raise AssertionError("User role not recognized")

        serializer = serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ListProfilesViewset(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'CL':
            queryset = TherapistProfile.objects.all()  # List all therapist profiles
        elif user.role == 'TH':
            queryset = ClientProfile.objects.all()  # List all client profiles
        else:
            raise AssertionError("User role not recognized")

        return queryset

    @action(detail=False, methods=['get'])
    def list_profiles(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        user = self.request.user
        if user.role == 'CL':
            return TherapistProfileSerializer
        elif user.role == 'TH':
            return ClientProfileSerializer
        else:
            raise NotFound('User role not found')

class DetailListViewset(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'CL':
            queryset = TherapistProfile.objects.all()
        elif user.role == 'TH':
            queryset = ClientProfile.objects.all()
        else:
            raise AssertionError("User role not recognized")

        return queryset

    @action(detail=True, methods=['get'])
    def detail_list(self, request, pk=None):
        queryset = self.get_queryset()
        profile = get_object_or_404(queryset, pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(profile)
        return Response(serializer.data)

    def get_serializer_class(self):
        user = self.request.user
        if user.role == 'CL':
            return TherapistProfileSerializer
        elif user.role == 'TH':
            return ClientProfileSerializer
        else:
            raise NotFound('User role not found')

class DeleteProfileViewset(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['delete'])
    def delete_profile(self, request):
        user = self.request.user
        if user.role == 'CL':
            profile = get_object_or_404(ClientProfile, client=user)
            serializer = ClientProfileSerializer(profile)
        elif user.role == 'TH':
            profile = get_object_or_404(TherapistProfile, therapist=user)
            serializer = TherapistProfileSerializer(profile)
            
        else:
            raise AssertionError("User role not recognized")
        profile.delete()
        return Response({'message': 'Profile deleted successfully'})

    def get_serializer_class(self):
        user = self.request.user
        if user.role == 'CL':
            return ClientProfileSerializer
        elif user.role == 'TH':
            return TherapistProfileSerializer
        else:
            raise NotFound('User role not found')