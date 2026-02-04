# system_settings/urls.py
from django.urls import path
from .views import SystemSecurityConfigurationView, NotificationEmailConfigurationView

urlpatterns = [
    path("system-security/", SystemSecurityConfigurationView.as_view(), name="system-security"),
    path("notifications-email/", NotificationEmailConfigurationView.as_view(), name="notifications-email"),
]
