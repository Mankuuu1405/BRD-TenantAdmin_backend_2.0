from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    FinancialYear,
    AssessmentYear,
    ReportingPeriod,
    Holiday,
    WorkingDay,
    WorkingHour,
    Overtime,
)
from .serializers import (
    FinancialYearSerializer,
    AssessmentYearSerializer,
    ReportingPeriodSerializer,
    HolidaySerializer,
    WorkingDaySerializer,
    WorkingHourSerializer,
    OvertimeSerializer,
)
from .utils import (
    yearly_view,
    half_yearly_view,
    quarterly_view,
    monthly_view,
)


class FinancialYearViewSet(viewsets.ModelViewSet):
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer

    @action(detail=True, methods=["get"], url_path="view")
    def view_modes(self, request, pk=None):
        fy = self.get_object()
        mode = request.query_params.get("mode", "yearly")

        if mode == "yearly":
            data = yearly_view(fy)
        elif mode == "half-yearly":
            data = half_yearly_view(fy)
        elif mode == "quarterly":
            data = quarterly_view(fy)
        elif mode == "monthly":
            data = monthly_view(fy)
        else:
            return Response({"error": "Invalid mode"}, status=400)

        return Response({
            "financial_year": fy.name,
            "view_mode": mode,
            "periods": data,
        })


class AssessmentYearViewSet(viewsets.ModelViewSet):
    queryset = AssessmentYear.objects.all()
    serializer_class = AssessmentYearSerializer


class ReportingPeriodViewSet(viewsets.ModelViewSet):
    queryset = ReportingPeriod.objects.all()
    serializer_class = ReportingPeriodSerializer


class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer


class WorkingDayViewSet(viewsets.ModelViewSet):
    queryset = WorkingDay.objects.all()
    serializer_class = WorkingDaySerializer


class WorkingHourViewSet(viewsets.ModelViewSet):
    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer


class OvertimeViewSet(viewsets.ModelViewSet):
    queryset = Overtime.objects.all()
    serializer_class = OvertimeSerializer
