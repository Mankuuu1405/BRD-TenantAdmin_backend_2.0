from django.urls import path
from .views import LoanAccountListAPIView

urlpatterns = [
    path("", LoanAccountListAPIView.as_view(), name="loan-account-list"),
]
