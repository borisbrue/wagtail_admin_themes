from django import forms
from django.conf import settings
from wagtail.admin.views.account import BaseSettingsPanel
from .models import CustomUserProfile
import os
from os import listdir
from os.path import isfile, join

# from wagtail.contrib.settings.views import BaseSettingsPanel


class CustomUserSettingsForm(forms.ModelForm):
    css_file = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = CustomUserProfile
        fields = ["css_file"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css_dir = os.path.join(
            os.path.dirname(__file__), "static", "css", "admin-themes"
        )
        css_files = [
            (f, f)
            for f in listdir(css_dir)
            if os.path.isfile(os.path.join(css_dir, f)) and f.endswith(".css")
        ]
        self.fields["css_file"].choices = [("", "---")] + css_files

        try:
            admin_theme = CustomUserProfile.objects.get(user_profile=self.instance)
        except CustomUserProfile.DoesNotExist:
            admin_theme = None
        if admin_theme:
            self.fields["css_file"].initial = admin_theme.css_file

    def save(self, commit=True):

        css_file = self.cleaned_data["css_file"]
        profile = super().save(commit=False)
        try:
            admin_theme = CustomUserProfile.objects.get(user_profile=profile)
        except CustomUserProfile.DoesNotExist:
            admin_theme = CustomUserProfile.objects.create(
                user_profile=profile, css_file=""
            )

        admin_theme.css_file = css_file
        admin_theme.save()

        if commit:
            profile.save()
        return profile


class CustomUserSettingsPanel(BaseSettingsPanel):
    name = "wagtail_admin_theme_css"
    title = "Admin Theme Css"
    order = 500
    form_class = CustomUserSettingsForm
    form_object = "profile"
