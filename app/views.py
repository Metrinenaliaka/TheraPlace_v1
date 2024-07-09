"""
my viewsets for the app
"""
from rest_framework import permissions, mixins, viewsets
from .serializers import ClientSerializer, TherapistSerializer, ClientSignupSerializer, TherapistSignupSerializer
from .models import Client, Therapist


class ClientViewSet(viewsets.ModelViewSet):
    """
    viewset for the client model
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

class TherapistViewSet(viewsets.ModelViewSet):
    """
    viewset for the therapist model
    """
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClientSignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    signup for client
    """
    queryset = Client.objects.all()
    serializer_class = ClientSignupSerializer

class TherapistSignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    signup for therapist
    """
    queryset = Therapist.objects.all()
    serializer_class = TherapistSignupSerializer
