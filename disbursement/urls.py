from django.urls import path
from .views import DisbursementQueueAPIView, DisburseLoanAPIView

urlpatterns = [
    path('disbursement-queue/', DisbursementQueueAPIView.as_view()),
    path('disburse-loan/<int:application_id>/', DisburseLoanAPIView.as_view()),
]
