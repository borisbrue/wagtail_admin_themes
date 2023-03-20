from django.db import models
from wagtail.users.models import UserProfile


class CustomUserProfile(models.Model):
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="admin_theme"
    )
    css_file = models.CharField(
        max_length=100,
        blank=True,
    )
