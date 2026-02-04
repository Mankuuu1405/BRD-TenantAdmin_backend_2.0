from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LoanApplicationViewSet,
    PropertyDetailViewSet,
    KYCDetailViewSet,
    CreditAssessmentViewSet,
)

router = DefaultRouter()

router.register(
    r'loan-applications',
    LoanApplicationViewSet,
    basename='loan-application'
)

router.register(
    r'property-details',
    PropertyDetailViewSet,
    basename='property-detail'
)

router.register(
    r'kyc-documents',
    KYCDetailViewSet,
    basename='kyc-document'
)

router.register(
    r'credit-assessments',
    CreditAssessmentViewSet,
    basename='credit-assessment'
)

urlpatterns = [
    path('', include(router.urls)),
]
