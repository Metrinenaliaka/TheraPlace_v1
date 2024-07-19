"""
Testing my views
"""
from .test_setup import TestAuthSetUp, TestProfileSetUp
from ..serializers import ClientProfileSerializer, TherapistProfileSerializer
from ..views import UpdateProfileViewset, ListProfilesViewset, DetailListViewset, DeleteProfileViewset
from ..models import ClientProfile, TherapistProfile


class TestViews(TestAuthSetUp):
    """
    This class tests my views for the project    
    """
    def test_signup_without_details(self):
        """
        test user signup failure without data
        """
        response = self.client.post(self.signup_url)
        self.assertEqual(response.status_code, 400)

    def test_signup(self):
        """
        test user signup
        """
        response = self.client.post(self.signup_url, self.data)
        self.assertEqual(response.status_code, 201)
    
    def test_invalid_login(self):
        """
        test user login with invalid data
        """
        res = self.client.post(self.signup_url, self.data, format='json')
        response = self.client.post(self.login_url, self.invalid_data, format='json')
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 401)
    
    def test_login(self):
        """
        test user login
        """
        res = self.client.post(self.signup_url, self.data, format='json')
        response = self.client.post(self.login_url, self.data, format='json')
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 200)
    
class TestProfileViews(TestProfileSetUp):
    """
    Tests availability of user profile
    """
    def test_update_profile_client(self):
        """
        test update for clients
        """
        res = self.client.post(self.signup_url, self.data, format='json')
        login_response = self.client.post(self.login_url, self.data, format='json')
        token = login_response.data.get('token')  # Extract token from login response

        if not token:
            self.fail("No token returned in login response")

        if self.role != 'CL' and self.role != 'TH':
            self.skipTest("Skipping profile test for user with undefined role.")

        view = UpdateProfileViewset.as_view({'post': 'update_profile'})
        request_data = self.client_data if self.role == 'CL' else self.therapist_data

        request = self.factory.post(self.update_profile_url, request_data, format='json', HTTP_AUTHORIZATION='Token ' + token)
        response = view(request)
        # import pdb
        # pdb.set_trace()

        self.assertEqual(response.status_code, 200)

    def test_list_profiles(self):
        """
        test list profiles
        """
        res = self.client.post(self.signup_url, self.data, format='json')
        login_response = self.client.post(self.login_url, self.data, format='json')
        token = login_response.data.get('token')

        if not token:
            self.fail("No token returned in login response")

        view = ListProfilesViewset.as_view({'get': 'list_profiles'})
        request = self.factory.get(self.list_profiles_url, HTTP_AUTHORIZATION='Token ' + token) 
        response = view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_detail_list(self):
        """
        test list profiles
        """
        res = self.client.post(self.signup_url, self.data, format='json')
        login_response = self.client.post(self.login_url, self.data, format='json')
        token = login_response.data.get('token')
        
        if not token:
            self.fail("No token returned in login response")
        
        profile = None
        if TherapistProfile.objects.exists():
            profile = TherapistProfile.objects.first()
            # detail_list_url = reverse('detail_list', kwargs={'pk': profile.pk})
        elif ClientProfile.objects.exists():
            profile = ClientProfile.objects.first()
            # detail_list_url = reverse('detail_list', kwargs={'pk': profile.pk})

        # Ensure a profile exists for testing
        if not profile:
            self.fail("No profile found for testing")

        view = DetailListViewset.as_view({'get': 'detail_list'})
        request = self.factory.get(self.detail_list_url, HTTP_AUTHORIZATION='Token ' + token) 
        response = view(request, profile.pk)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 200)
    
    def test_delete_profile(self):
        """
        test delete profile
        """
        res = self.client.post(self.signup_url, self.data, format='json')
        login_response = self.client.post(self.login_url, self.data, format='json')
        token = login_response.data.get('token')

        if not token:
            self.fail("No token returned in login response")

        view = DeleteProfileViewset.as_view({'post': 'delete_profile'})
        request = self.factory.post(self.delete_profile_url, HTTP_AUTHORIZATION='Token ' + token) 
        response = view(request)
        self.assertEqual(response.status_code, 204)
   