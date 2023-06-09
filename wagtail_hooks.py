from wagtail.core import hooks
from wagtail_tenants.utils import (
    get_allowed_features,
    get_tenant_aware_apps,
)
from .panels import CustomUserSettingsPanel


@hooks.register("register_account_settings_panel")
def register_custom_settings_panel(request, user, profile):
    return CustomUserSettingsPanel(request, user, profile)
