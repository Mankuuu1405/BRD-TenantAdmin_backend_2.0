from rest_framework import serializers
from .models import Mandate


class MandateSerializer(serializers.ModelSerializer):
    application_id = serializers.CharField(
        source="loan_application.application_id",
        read_only=True
    )

    customer_name = serializers.CharField(
        source="loan_application.customer.full_name",
        read_only=True
    )

    penny_drop_status_label = serializers.CharField(
        source="get_penny_drop_status_display",
        read_only=True
    )

    enach_status_label = serializers.CharField(
        source="get_enach_status_display",
        read_only=True
    )

    bank_details = serializers.SerializerMethodField()

    class Meta:
        model = Mandate
        fields = [
            "id",
            "application_id",
            "customer_name",
            "bank_details",
            "penny_drop_status",
            "penny_drop_status_label",
            "enach_status",
            "enach_status_label",
        ]

    def get_bank_details(self, obj):
        bank_detail = getattr(obj.loan_application, "bank_detail", None)
        if not bank_detail:
            return None
        
        return {
        "bank_name": bank_detail.bank_name,
        "account_number": bank_detail.account_number,
        "ifsc_code": bank_detail.ifsc_code,
    }

