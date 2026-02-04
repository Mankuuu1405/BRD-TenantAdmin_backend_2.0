from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FinancialYearViewSet,
    AssessmentYearViewSet,
    ReportingPeriodViewSet,
    HolidayViewSet,
    WorkingDayViewSet,
    WorkingHourViewSet,
    OvertimeViewSet,
)

router = DefaultRouter()
router.register("financial-years", FinancialYearViewSet)
router.register("assessment-years", AssessmentYearViewSet)
router.register("reporting-periods", ReportingPeriodViewSet)
router.register("holidays", HolidayViewSet)
router.register("working-days", WorkingDayViewSet)
router.register("working-hours", WorkingHourViewSet)
router.register("overtime", OvertimeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
