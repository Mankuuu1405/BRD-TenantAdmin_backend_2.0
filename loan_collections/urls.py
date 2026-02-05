from django.urls import path
from .views import (
    CollectionStatsAPIView,
    OverdueLoansAPIView,
)

urlpatterns = [
    path("stats/", CollectionStatsAPIView.as_view()),
    path("overdue-loans/", OverdueLoansAPIView.as_view()),
]
