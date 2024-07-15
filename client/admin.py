"""
This file is used to register the models in the Django admin panel.
"""
from django.contrib import admin

from client.models import TherapistProfile, ClientProfile

admin.site.register(ClientProfile)
admin.site.register(TherapistProfile)
