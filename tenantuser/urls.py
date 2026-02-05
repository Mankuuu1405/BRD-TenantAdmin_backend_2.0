from django.urls import path
from .views import TenantUserCreateView, TenantUserListView

urlpatterns = [
    path("users/", TenantUserListView.as_view(), name="tenant-user-list"),
    path("users/create/", TenantUserCreateView.as_view(), name="tenant-user-create"),
]
