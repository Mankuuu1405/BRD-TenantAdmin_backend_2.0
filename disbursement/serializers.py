from rest_framework import serializers
from .models import Disbursement

class DisbursementQueueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="loan_application.id")
    name = serializers.SerializerMethodField()
    bank = serializers.SerializerMethodField()
    ifsc = serializers.SerializerMethodField()

    class Meta:
        model = Disbursement
        fields = [
            "id",
            "name",
            "amount",
            "bank",
            "ifsc",
        ]

    def get_name(self, obj):
        la = obj.loan_application
        return (
            getattr(la, "applicant_name", None)
            or getattr(la, "customer_name", None)
            or getattr(la, "full_name", "")
        )

    def get_bank(self, obj):
        la = obj.loan_application
        return (
            getattr(la, "bank_name", None)
            or getattr(la, "bank", "")
        )

    def get_ifsc(self, obj):
        la = obj.loan_application
        return (
            getattr(la, "ifsc_code", None)
            or getattr(la, "ifsc", "")
        )
