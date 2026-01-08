from django.contrib import admin
from .models import Mandate

@admin.register(Mandate)
class MandateAdmin(admin.ModelAdmin):
    list_display = (
        'loan_application',
        'penny_drop_status',
        'enach_status',
        'verified_at'
    )
