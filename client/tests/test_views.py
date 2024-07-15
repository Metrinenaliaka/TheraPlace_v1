"""
Testing my views
"""
from .test_setup import TestAuthSetUp, TestProfileSetUp
from ..serializers import ClientProfileSerializer, TherapistProfileSerializer
from ..views import UpdateProfileViewset


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
        if self.role != 'CL':
            if self.role != 'TH':
                self.skipTest("Skipping client profile test for non-therapist user.")
            view = UpdateProfileViewset.as_view({'post': 'update_profile'})
            request = self.factory.post(self.update_profile_url, self.therapist_data, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
            # request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
            response = view(request)
            import pdb
            pdb.set_trace()
            self.assertEqual(response.status_code, 200)
        else:
            if self.role != 'CL':
                self.skipTest("Skipping therapist profile test for non-client user.")
            view = UpdateProfileViewset.as_view({'post': 'update_profile'})
            request = self.factory.post(self.update_profile_url, self.client_data, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
            import pdb
            pdb.set_trace()
            # request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
            response = view(request)
            self.assertEqual(response.status_code, 200)
    
    # def test_update_profile_therapist(self):
    #     """
    #     test update for clients
    #     """
    #     res = self.client.post(self.signup_url, self.data, format='json')
    #     login_response = self.client.post(self.login_url, self.data, format='json')
    #     if self.role != 'TH':
    #         self.skipTest("Skipping client profile test for non-therapist user.")
    #     view = UpdateProfileViewset.as_view({'post': 'update_profile'})
    #     request = self.factory.post(self.update_profile_url, self.therapist_data, format='json')
    #     request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
    #     response = view(request)
    #     self.assertEqual(response.status_code, 200)