"""
This module contains the views for the client app.
The endpoints are done using viewsets and actions.
"""
from django.urls import reverse
from rest_framework import viewsets, status, permissions, authentication
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework.exceptions import NotFound
from .models import ClientUser, ClientProfile, TherapistProfile, Appointments
from .serializers import ClientUserSerializer, ClientProfileSerializer, TherapistProfileSerializer, LoginSerializer, DefaultProfileSerializer, AppointmentSerializer

User = get_user_model()

class LoginViewset(viewsets.GenericViewSet):
    """
    Handles login and potentially retrieves user profile data.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        function handles user login
        """
        # validation the input data
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
            # redirect_url = f"{reverse('update_profile')}?token={token.key}"
            # return redirect(redirect_url)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class SignUpViewset(viewsets.GenericViewSet):
    """
    handles user signups
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = ClientUserSerializer

    def post(self, request):
        """
        gets the credentials and logs in the user
        """
        serializer = ClientUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutViewset(viewsets.GenericViewSet):
    """
    custom logout
    """
    serializer_class = DefaultProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        function logs out the user
        """
        request.user.auth_token.delete()
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
class UpdateProfileViewset(viewsets.GenericViewSet):
    """
    This allows users to update their profiles
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        we overide serialiser class to get the correct serializer
        """
        try:
            user = self.request.user

        except AttributeError:
            return DefaultProfileSerializer
        if user.role == 'CL':
            serializer_class = ClientProfileSerializer
        elif user.role == 'TH':
            serializer_class = TherapistProfileSerializer
        else:
            raise AssertionError("User role not recognized")
        return serializer_class

    @action(detail=False, methods=['post'])
    def update_profile(self, request):
        """
        function updates the user details
        """
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
    """
    a logged in client can view profiles for other users
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        returns the queryset based on the user role
        """
        user = self.request.user

        if user.role == 'CL':
            queryset = TherapistProfile.objects.all()
        elif user.role == 'TH':
            queryset = ClientProfile.objects.all()
        else:
            raise AssertionError("User role not recognized")

        return queryset

    @action(detail=False, methods=['get'])
    def list_profiles(self, request):
        """
        function lists all the profiles
        """
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        """
        returns the correct serializer based on the user role
        """
        try:
            user = self.request.user

        except AttributeError:
            return DefaultProfileSerializer

        if user.role == ClientUser.Role.CLIENT:
            return TherapistProfileSerializer
        elif user.role == ClientUser.Role.THERA:
            return ClientProfileSerializer
        else:
            raise NotFound('User role not found')

class DetailListViewset(viewsets.GenericViewSet):
    """
    A logged in user can view the details of another user
    """
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'CL':
            queryset = ClientProfile.objects.all()
        elif user.role == 'TH':
            queryset = TherapistProfile.objects.all()
        else:
            raise AssertionError("User role not recognized")

        return queryset

    @action(detail=True, methods=['get'])
    def detail_list(self, request, pk=None):
        """
        function lists the details of a user
        """
        queryset = self.get_queryset()
        profile = get_object_or_404(queryset, pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(profile)
        return Response(serializer.data)

    def get_serializer_class(self):
        """
        returns the correct serializer based on the user role
        """
        try:
            user = self.request.user

        except AttributeError:
            return DefaultProfileSerializer
        if user.role == ClientUser.Role.CLIENT:
            return ClientProfileSerializer
        elif user.role == ClientUser.Role.THERA:
            return TherapistProfileSerializer
        else:
            raise NotFound('User role not found')

class DeleteProfileViewset(viewsets.GenericViewSet):
    """
    deletes a user and their profile
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DefaultProfileSerializer

    def get_queryset(self):
        """
        returns the queryset based on the user role
        """
        user = self.request.user
        if user.role == ClientUser.Role.CLIENT:
            return ClientProfile.objects.filter(client=user)
        elif user.role == ClientUser.Role.THERA:
            return TherapistProfile.objects.filter(therapist=user)
        else:
            raise AssertionError("User role not recognized")

    @action(detail=False, methods=['delete'])
    def delete_profile(self, request):
        """
        function deletes the user and their profile
        """
        user = self.request.user
        if user.role == ClientUser.Role.CLIENT:
            profile = ClientProfile.objects.filter(client=user).first()
        elif user.role == ClientUser.Role.THERA:
            profile = TherapistProfile.objects.filter(therapist=user).first()
        else:
            return Response({"detail": "User role not recognized"},
                            status=status.HTTP_400_BAD_REQUEST)

        if profile:
            profile.delete()
            user.delete()
            return Response({"detail": "Profile and user deleted successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

class AppointmentViewset(viewsets.GenericViewSet):
    """
    Handles setting up of appointments
    """
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Appointments.objects.all()

    @action(detail=False, methods=['post'])
    def set_appointment(self, request):
        """
        function sets up an appointment
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TherapistProfileViewSet(viewsets.ModelViewSet):
    """
    Helps with the response to a therapist appointment
    """
    queryset = TherapistProfile.objects.all()
    serializer_class = TherapistProfileSerializer
    lookup_field = 'pk'

    @action(detail=True, methods=['post'])
    def respond_to_appointment(self, request, pk=None):
        """
        This function responds to an appointment
        """
        therapist = self.get_object()
        appointment_id = request.data.get('appointment_id')
        response = request.data.get('response')

        if not appointment_id or not response:
            return Response({"detail": "Appointment ID and response are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the appointment
            appointment = Appointments.objects.get(id=appointment_id)
        except Appointments.DoesNotExist:
            return Response({"detail": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        if appointment.therapist.therapist.pk != therapist.pk:
            return Response({"detail": "This appointment does not belong to this therapist"},
                            status=status.HTTP_403_FORBIDDEN)

        therapist.respond_to_appointment(appointment_id, response)

        return Response({"detail": "Appointment Approved/Declined"}, status=status.HTTP_200_OK)
