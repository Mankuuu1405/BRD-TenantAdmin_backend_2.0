from rest_framework import serializers
from banking.models import Mandate
from los.models import BankDetail


class BankingDashboardSerializer(serializers.ModelSerializer):
    application_id = serializers.IntegerField(
        source="loan_application.id", read_only=True
    )
    customer = serializers.CharField(
        source="loan_application.customer.name", read_only=True
    )

    bank = serializers.SerializerMethodField()
    ifsc = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()

    penny_drop_status = serializers.CharField(read_only=True)
    enach_status = serializers.CharField(read_only=True)

    class Meta:
        model = Mandate   # ✅ FIXED
        fields = [
            "id",
            "application_id",
            "customer",
            "bank",
            "ifsc",
            "account",
            "penny_drop_status",
            "enach_status",
            "action",
    
        ]

    # -------------------------
    # Bank Details (via LoanApplication)
    # -------------------------
    def get_bank(self, obj):
        bank_detail = getattr(obj.loan_application, "bank_detail", None)
        return bank_detail.bank_name if bank_detail else None

    def get_ifsc(self, obj):
        bank_detail = getattr(obj.loan_application, "bank_detail", None)
        return bank_detail.ifsc_code if bank_detail else None

    def get_account(self, obj):
        bank_detail = getattr(obj.loan_application, "bank_detail", None)
        if bank_detail and bank_detail.account_number:
            return f"XXXXXX{bank_detail.account_number[-4:]}"
        return None


# ---------------------------------------
# Serializer for BankDetail (masked account)
# ---------------------------------------
class BankAccountOnlySerializer(serializers.ModelSerializer):
    account_number = serializers.SerializerMethodField()

    class Meta:
        model = BankDetail
        fields = ["account_number"]

    def get_account_number(self, obj):
        return f"XXXXXX{obj.account_number[-4:]}" if obj.account_number else None
