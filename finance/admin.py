from django.contrib import admin
from .models import (
    FinancialYear,
    AssessmentYear,
    ReportingPeriod,
    Holiday,
    WorkingDay,
    WorkingHour,
    Overtime,
)


@admin.register(FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "status")
    list_filter = ("status",)
    ordering = ("-start_date",)


@admin.register(AssessmentYear)
class AssessmentYearAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "financial_year",
        "status",
        "financial_eligibility_years",
        "itr_years_required",
        "credit_assessment_enabled",
    )
    list_filter = ("status", "credit_assessment_enabled")



@admin.register(ReportingPeriod)
class ReportingPeriodAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ("date", "title")
    ordering = ("date",)


@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ("day", "is_working")


@admin.register(WorkingHour)
class WorkingHourAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time")


@admin.register(Overtime)
class OvertimeAdmin(admin.ModelAdmin):
    list_display = ("enabled", "rate_multiplier")
