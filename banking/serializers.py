from rest_framework import serializers
from los.models import LoanApplication, BankDetail

# ---------------------------------------
# Serializer for LoanApplication / Dashboard
# ---------------------------------------
class BankingDashboardSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source="customer.name")
    bank = serializers.SerializerMethodField()
    ifsc = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()

    def get_bank(self, obj):
        return obj.bank_detail.bank_name if obj.bank_detail else None

    def get_ifsc(self, obj):
        return obj.bank_detail.ifsc_code if obj.bank_detail else None

    def get_account(self, obj):
        return obj.bank_detail.account_number if obj.bank_detail else None

    class Meta:
        model = LoanApplication
        fields = [
            "id",
            "customer",
            "bank",
            "ifsc",
            "account",
        ]

# ---------------------------------------
# Serializer for BankDetail (masked account)
# ---------------------------------------
class BankAccountOnlySerializer(serializers.ModelSerializer):
    account_number = serializers.SerializerMethodField()

    class Meta:
        model = BankDetail
        fields = ["account_number"]

    def get_account_number(self, obj):
        # Mask all but last 4 digits for privacy
        return f"XXXXXX{obj.account_number[-4:]}" if obj.account_number else None
