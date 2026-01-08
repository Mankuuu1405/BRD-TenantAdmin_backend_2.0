from rest_framework import serializers
from .models import LoanApplication, KYCDetail, CreditAssessment, PropertyDetail

try:
    from .models import ApplicationStatusLog
except ImportError:
    ApplicationStatusLog = None


# ============================================================
# KYC DETAIL SERIALIZER
# ============================================================
class KYCDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCDetail
        fields = "__all__"
        read_only_fields = ("status", "uploaded_at")


# ============================================================
# CREDIT ASSESSMENT SERIALIZER
# ============================================================
class CreditAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditAssessment
        fields = "__all__"
        read_only_fields = "__all__"


# ============================================================
# PROPERTY DETAIL SERIALIZER
# ============================================================
class PropertyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDetail
        fields = "__all__"


# ============================================================
# LOAN APPLICATION SERIALIZER
# ============================================================
class LoanApplicationSerializer(serializers.ModelSerializer):

    # Nested relations (THIS IS ALL YOU NEED)
    documents = KYCDetailSerializer(many=True, read_only=True)
    credit_assessment = CreditAssessmentSerializer(read_only=True)
    property_detail = PropertyDetailSerializer(read_only=True)

    # Display-only fields
    tenant_name = serializers.CharField(source="tenant.name", read_only=True)
    customer_name = serializers.CharField(source="customer.first_name", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = LoanApplication
        fields = "__all__"
        read_only_fields = (
            "application_id",
            "tenant",
            "created_by",
            "created_at",
            "foir_percentage",
            "net_cash_flow",
        )

    # ===============================
    # NORMALIZE RAW INPUT
    # ===============================
    def to_internal_value(self, data):
        data = data.copy()

        if data.get("income_type"):
            data["income_type"] = (
                data["income_type"]
                .upper()
                .replace(" ", "_")
                .replace("-", "_")
            )

        if data.get("borrower_type"):
            data["borrower_type"] = (
                data["borrower_type"]
                .upper()
                .replace(" ", "_")
                .replace("-", "_")
            )

        return super().to_internal_value(data)


    # ========================================================
    # BUSINESS VALIDATION
    # ========================================================
    def validate(self, attrs):
        income_type = attrs.get("income_type")
        borrower_type = attrs.get("borrower_type")
        product = attrs.get("product")

        if income_type == "SALARIED" and not attrs.get("employer_name"):
            raise serializers.ValidationError(
                {"employer_name": "Employer name is required for salaried applicants."}
            )

        if income_type == "SELF_EMPLOYED" and not attrs.get("business_name"):
            raise serializers.ValidationError(
                {"business_name": "Business name is required for self-employed applicants."}
            )

        if borrower_type in ["PARTNERSHIP", "CORPORATE"] and not attrs.get("business_name"):
            raise serializers.ValidationError(
                {"business_name": "Business name is mandatory for non-individual borrowers."}
            )

        # Property validation ONLY for Mortgage Loan
        if product and product.loan_type == "MORTGAGE":
            if self.instance and self.instance.status in ["UNDERWRITING", "SANCTIONED"]:
                if not hasattr(self.instance, "property_detail"):
                    raise serializers.ValidationError(
                        {"property_detail": "Property details are required for Mortgage Loan."}
            )


        return attrs

    # ========================================================
    # STATUS TRANSITION CONTROL
    # ========================================================
    def update(self, instance, validated_data):
        request = self.context.get("request")
        user = request.user if request else None

        new_status = validated_data.get("status")
        old_status = instance.status

        allowed_transitions = {
            "NEW": ["KNOCKOUT_PENDING", "REJECTED"],
            "KNOCKOUT_PENDING": ["DOC_UPLOAD", "REJECTED"],
            "DOC_UPLOAD": ["UNDERWRITING", "REJECTED"],
            "UNDERWRITING": ["SANCTIONED", "HOLD", "REJECTED"],
            "HOLD": ["UNDERWRITING", "REJECTED"],
            "SANCTIONED": ["PRE_DISBURSEMENT"],
            "PRE_DISBURSEMENT": ["DISBURSED"],
        }

        if new_status and new_status != old_status:
            if new_status not in allowed_transitions.get(old_status, []):
                raise serializers.ValidationError(
                    f"Invalid status transition: {old_status} → {new_status}"
                )

            if ApplicationStatusLog:
                ApplicationStatusLog.objects.create(
                    application=instance,
                    old_status=old_status,
                    new_status=new_status,
                    changed_by=user,
                )

        return super().update(instance, validated_data)
