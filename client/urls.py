
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from client import views

# router = DefaultRouter()
# router.register(r'users', views.ProfileViewSet, basename='users')
# router.register(r'register', views.SignUpViewset, basename='signup')
# router.register(r'auth', views.LoginViewset, basename='login')

urlpatterns = [
    path('login/', views.LoginViewset.as_view({'post': 'login'})),
    path('register/', views.SignUpViewset.as_view({'post': 'post'})),
    path('update-profile/', views.UpdateProfileViewset.as_view({'post': 'update_profile'})),
    path('list-profiles/', views.ListProfilesViewset.as_view({'get': 'list_profiles'})),
    path('profile/<int:pk>/', views.DetailListViewset.as_view({'get': 'detail_list'})),
    path('delete/', views.DeleteProfileViewset.as_view({'post': 'delete_profile'})),
]