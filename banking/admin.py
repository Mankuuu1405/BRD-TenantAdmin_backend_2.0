from django.contrib import admin
from .models import Mandate


@admin.register(Mandate)
class MandateAdmin(admin.ModelAdmin):
    list_display = (
        "application_id",
        "customer_name",
        "penny_drop_status",
        "enach_status",
        "action",
        "updated_at",
    )

    list_editable = (
        "penny_drop_status",
        "enach_status",
        "action",
    )

    list_select_related = ("loan_application", "loan_application__customer")

    # -------------------------
    # Custom display fields
    # -------------------------
    @admin.display(description="Application ID")
    def application_id(self, obj):
        return obj.loan_application.id

    @admin.display(description="Customer")
    def customer_name(self, obj):
        customer = obj.loan_application.customer
        return (
            getattr(customer, "full_name", None)
            or getattr(customer, "name", None)
            or getattr(customer, "applicant_name", None)
            or f"{getattr(customer, 'first_name', '')} {getattr(customer, 'last_name', '')}".strip()
        )
