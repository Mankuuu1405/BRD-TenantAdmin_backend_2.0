from django.contrib import admin

from .models import (
    LoanApplication,
    KYCDetail,
    CreditAssessment,
    PropertyDetail,
    MortgageUnderwriting,
    BankDetail,
)

# ============================================================
# PROPERTY DETAIL INLINE (ONLY FOR MORTGAGE LOANS)
# ============================================================
class PropertyDetailInline(admin.StackedInline):
    model = PropertyDetail
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        """
        Allow PropertyDetail ONLY IF:
        - LoanApplication exists
        - Loan is Mortgage
        - PropertyDetail does not already exist
        """
        if not obj:
            return False

        if not obj.is_mortgage_loan():
            return False

        if hasattr(obj, "property_detail"):
            return False

        return True

    def has_change_permission(self, request, obj=None):
        return bool(obj and obj.is_mortgage_loan())

    def has_delete_permission(self, request, obj=None):
        return bool(obj and obj.is_mortgage_loan())


# ============================================================
# KYC DETAIL INLINE
# ============================================================
class KYCDetailInline(admin.TabularInline):
    model = KYCDetail
    extra = 1


# ============================================================
# CREDIT ASSESSMENT INLINE
# ============================================================
class CreditAssessmentInline(admin.StackedInline):
    model = CreditAssessment
    extra = 0
    can_delete = False
    readonly_fields = ("status", "created_at", "updated_at")


# ============================================================
# MORTGAGE UNDERWRITING INLINE
# ============================================================
class MortgageUnderwritingInline(admin.StackedInline):
    model = MortgageUnderwriting
    extra = 0
    can_delete = False
    readonly_fields = (
        "property_market_value",
        "ltv_on_property",
        "final_eligible_amount",
        "approved_at",
    )


# ============================================================
# LOAN APPLICATION ADMIN
# ============================================================
@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "application_id",
        "first_name",
        "mobile_no",
        "status",
        "created_at",
    )

    list_display_links = ("application_id",)
    list_filter = ("status", "income_type", "product")
    search_fields = (
        "application_id",
        "customer__first_name",
        "customer__last_name",
        "pan_number",
        "mobile_no",
    )

    readonly_fields = (
        'application_id',
        'created_at',
    )   

    inlines = [
        KYCDetailInline,
        CreditAssessmentInline,
        PropertyDetailInline,
        MortgageUnderwritingInline,
    ]

    def save_model(self, request, obj, form, change):
        if not change and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# ============================================================
# CREDIT ASSESSMENT ADMIN
# ============================================================
@admin.register(CreditAssessment)
class CreditAssessmentAdmin(admin.ModelAdmin):
    list_display = ("application", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = (
        "application__application_id",
        "application__customer__first_name",
    )
    readonly_fields = ("status", "created_at", "updated_at")


# ============================================================
# PROPERTY DETAIL ADMIN
# ============================================================
@admin.register(PropertyDetail)
class PropertyDetailAdmin(admin.ModelAdmin):
    list_display = (
        "loan_application",
        "property_type",
        "city",
        "created_at",
    )
    autocomplete_fields = ("loan_application",)


# ============================================================
# MORTGAGE UNDERWRITING ADMIN
# ============================================================
@admin.register(MortgageUnderwriting)
class MortgageUnderwritingAdmin(admin.ModelAdmin):
    list_display = (
        "loan_application",
        "property_market_value",
        "ltv_on_property",
        "final_eligible_amount",
        "approved_at",
    )
    search_fields = (
        "loan_application__application_id",
        "loan_application__customer__first_name",
    )
    readonly_fields = (
        "property_market_value",
        "ltv_on_property",
        "final_eligible_amount",
        "approved_at",
    )
@admin.register(BankDetail)
class BankDetailAdmin(admin.ModelAdmin):
    list_display = ('loan_application', 'bank_name', 'account_number', 'ifsc_code', 'created_at')
    search_fields = ('loan_application__application_id', 'bank_name', 'account_number')