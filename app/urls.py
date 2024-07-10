from django.urls import include, path
# from django.contrib import admin
from rest_framework import routers
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token 
from app import views

router = routers.DefaultRouter()
router.register(r'signup', views.SignupViewSet, basename='signup')
router.register(r'auth', views.LoginViewSet, basename='login')
router.register(r'profiles', views.ProfileViewSet, basename='profile')


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
