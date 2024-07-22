"""
tests for my models
"""
from .test_setup import TestModelsSetUp


class TestClientUser(TestModelsSetUp):
    """
    This class tests ClientUser model
    """
    def test_client_user_creation(self):
        """
        test client user creation
        """
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.data['username'], self.data['username'])
        self.assertEqual(response.data['email'], self.data['email'])
        self.assertEqual(response.data['role'], self.data['role'])
        self.assertEqual(response.status_code, 201)

class TestClientProfile(TestModelsSetUp):
    """
    This class tests ClientUser model
    """
    def test_client_user_creation(self):
        """
        test client user creation
        """
        response = self.client.post(self.update_profile_url, self.data, format='json')
        self.assertEqual(response.data['username'], self.data['username'])
        self.assertEqual(response.data['email'], self.data['email'])
        self.assertEqual(response.data['role'], self.data['role'])
        self.assertEqual(response.status_code, 201)