"""
This are uls for the endpoints
"""
from django.urls import path
from client import views

urlpatterns = [
    path('login/', views.LoginViewset.as_view({'post': 'login'}), name='login'),
    path('register/', views.SignUpViewset.as_view({'post': 'post'}), name='register'),
    path('update-profile/', views.UpdateProfileViewset.as_view({'post': 'update_profile'}),
         name='update_profile'),
    path('list-profiles/', views.ListProfilesViewset.as_view({'get': 'list_profiles'}),
         name='list_profiles'),
    path('profile/<int:pk>/', views.DetailListViewset.as_view({'get': 'detail_list'}),
         name='detail_list'),
    path('delete/', views.DeleteProfileViewset.as_view({'delete': 'delete_profile'}),
         name='delete_profile'),
    path('set-appointment/', views.AppointmentViewset.as_view({'post': 'set_appointment'}),
         name='set_appointment'),
    path('approve-app/<int:pk>/', views.TherapistProfileViewSet.as_view({'post': 'respond_to_appointment'}),
         name='approve_app'),
    path('logout/', views.LogoutViewset.as_view({'post': 'logout'}), name='logout'),
]
