from rest_framework import serializers
from .models import (
    FinancialYear,
    AssessmentYear,
    ReportingPeriod,
    Holiday,
    WorkingDay,
    WorkingHour,
    Overtime,
)


class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = "__all__"
        read_only_fields = ("name",)


class AssessmentYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentYear
        fields = "__all__"
        read_only_fields = ("name", "start_date", "end_date")



class ReportingPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingPeriod
        fields = "__all__"


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = "__all__"


class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingDay
        fields = "__all__"


class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = "__all__"


class OvertimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime
        fields = "__all__"
