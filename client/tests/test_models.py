"""
tests for my models
"""
from .test_setup import TestModelsSetUp
from ..models import ClientUser, ClientProfile, TherapistProfile, Appointments


class TestClientUser(TestModelsSetUp):
    """
    This class tests ClientUser model
    """
    def test_client_user_creation(self):
        """
        test client user creation
        """
        self.assertEqual(self.client_user.username, 'testuser')
        self.assertEqual(self.client_user.email, '