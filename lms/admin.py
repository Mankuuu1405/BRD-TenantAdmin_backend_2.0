from django.contrib import admin
from .models import LoanAccount

@admin.register(LoanAccount)
class LoanAccountAdmin(admin.ModelAdmin):
    list_display = (
        "disbursement",
        "status",
        "principal",
        "outstanding_principal",
        "created_at",
        "action",
    )

    list_filter = ("status",)
