from rest_framework import serializers
from .models import LoanAccount


class LoanAccountListSerializer(serializers.ModelSerializer):
    # LMS field: disbursement → API field: loan_account_id
    loan_account_id = serializers.UUIDField(
        source="disbursement",
        read_only=True
    )

    # LMS field: principal → API field: principal_amount
    principal_amount = serializers.DecimalField(
        source="principal",
        max_digits=14,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = LoanAccount
        fields = [
            "loan_account_id",
            "principal_amount",
            "outstanding_principal",
            "status",
            "created_at",
        ]
