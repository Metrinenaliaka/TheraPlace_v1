"""
Definition of the test class for the setup of the application.
"""
from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from faker import Faker
from ..models import ClientProfile, TherapistProfile

class TestAuthSetUp(APITestCase):
    """
    the class contains setup and teardown for AUTH
    """
    def setUp(self):
        """
        set up function
        """
        self.factory = APIRequestFactory()
        self.signup_url = reverse('register')
        self.login_url = reverse('login')
        self.update_profile_url = reverse('update_profile')
        
        self.fake = Faker()

        self.role = self.fake.random_element(elements=('CL', 'TH'))

        self.data = {
            'username': self.fake.user_name(),
            'email': self.fake.email(),
            'password': self.fake.password(),
            'role': self.role
        }
        self.invalid_data = {
            'username': self.fake.user_name(),
            'password': self.fake.password(),
        }
    
    def tearDown(self):
        """
        tear down function
        """
        return super().tearDown()


class TestProfileSetUp(APITestCase):
    """
    the class contains setup and teardown for PROFILE
    """
    def setUp(self):
        """
        set up function
        """
        self.factory = APIRequestFactory()
        self.signup_url = reverse('register')
        self.login_url = reverse('login')
        self.update_profile_url = reverse('update_profile')
        self.list_profiles_url = reverse('list_profiles')
        self.detail_list_url = reverse('detail_list', args=[1])
        self.delete_profile_url = reverse('delete_profile')
        
        self.fake = Faker()

        self.role = self.fake.random_element(elements=('CL', 'TH'))

        self.data = {
            'username': self.fake.user_name(),
            'email': self.fake.email(),
            'password': self.fake.password(),
            'role': self.role
        }
        self.invalid_data = {
            'username': self.fake.user_name(),
            'password': self.fake.password(),
        }
        self.user = get_user_model().objects.create_user(
            username=self.data['username'],
            email=self.data['email'],
            password=self.data['password'],
            role=self.data['role']
        )
        self.client_data = {
            'age': self.fake.random_int(min=1, max=100),
            'description': self.fake.text(),
            'condition': self.fake.text()
        }
        self.therapist_data = {
            'experience': self.fake.random_int(min=1, max=100),
            'description': self.fake.text(),
            'occupation': self.fake.text(),
            'price': self.fake.random_int(min=1, max=100),
            'location': self.fake.text()
        }

        self.token, created = Token.objects.get_or_create(user=self.user)

        if self.role == 'CL':
            self.client_profile = ClientProfile.objects.create(
                client=self.user,
                age=self.client_data['age'],
                description=self.client_data['description'],
                condition=self.client_data['condition']
            )
        elif self.role == 'TH':
            self.therapist_profile = TherapistProfile.objects.create(
                therapist=self.user,
                experience=self.therapist_data['experience'],
                description=self.therapist_data['description'],
                occupation=self.therapist_data['occupation'],
                price=self.therapist_data['price'],
                location=self.therapist_data['location']
            )
        self.client.force_login(self.user)
    
    def tearDown(self):
        """
        tear down function
        """
        return super().tearDown()