from django.contrib import admin
from .models import Disbursement

@admin.register(Disbursement)
class DisbursementAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'loan_application',
        'amount',
        'penny_drop_status',
        'enach_status',
        'created_at',
    )

    list_filter = (
        'penny_drop_status',
        'enach_status',
    )

    search_fields = (
        'loan_application__application_id',
    )
