from django.contrib import admin
from .models import Profile, ClientProfile, TherapistProfile

admin.site.register(Profile)
admin.site.register(ClientProfile)
admin.site.register(TherapistProfile)
