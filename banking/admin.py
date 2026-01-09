from django.contrib import admin
from .models import Mandate

@admin.register(Mandate)
class MandateAdmin(admin.ModelAdmin):
    list_display = (
        "application_id",
        "customer_name",
        "bank_details_status",
        "penny_drop_status",
        "enach_status",
    )

    def application_id(self, obj):
        return obj.loan_application.id

    def customer_name(self, obj):
        customer = obj.loan_application.customer
        return (
            getattr(customer, "full_name", None)
            or getattr(customer, "name", None)
            or getattr(customer, "applicant_name", None)
            or f"{getattr(customer, 'first_name', '')} {getattr(customer, 'last_name', '')}".strip()
        )

    def bank_details_status(self, obj):
        return "AVAILABLE" if hasattr(obj.loan_application, "bank_detail") else "MISSING"

    def penny_drop_status(self, obj):
        return obj.penny_drop_status

    def enach_status(self, obj):
        return obj.enach_status
