from django.urls import include, path
from rest_framework import routers
from app import views

router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'therapists', views.TherapistViewSet)
router.register(r'signup/client', views.ClientSignupViewSet, basename='client-signup')
router.register(r'signup/therapist', views.TherapistSignupViewSet, basename='therapist-signup')

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/', include('rest_framework.urls', namespace='rest_framework'))
]
