from django.contrib import admin
from .models import UserProfile, confirm_email

admin.site.register(UserProfile)
admin.site.register(confirm_email)