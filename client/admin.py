"""
This file is used to register the models in the Django admin panel.
"""
from django.contrib import admin

from client.models import TherapistProfile, ClientProfile, Appointments, ClientUser

admin.site.register(ClientProfile)
admin.site.register(TherapistProfile)
admin.site.register(Appointments)
admin.site.register(ClientUser)