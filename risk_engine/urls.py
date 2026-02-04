from django.urls import path
from .views import (
    CreditScoreRuleListCreateAPIView,
    NegativeAreaListCreateAPIView
)

urlpatterns = [
    path('risk/credit-rules/', CreditScoreRuleListCreateAPIView.as_view()),
    path('risk/negative-areas/', NegativeAreaListCreateAPIView.as_view()),
]
