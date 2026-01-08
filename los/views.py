from django.db import transaction

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    LoanApplication,
    KYCDetail,
    CreditAssessment,
    PropertyDetail,
)

from .serializers import (
    LoanApplicationSerializer,
    KYCDetailSerializer,
    CreditAssessmentSerializer,
    PropertyDetailSerializer,
)

from .logic.rule_engine import RuleEngine
from .logic.integrations import SmartVerificationService


# ============================================================
# LOAN APPLICATION VIEWSET (LOS CORE)
# ============================================================
class LoanApplicationViewSet(viewsets.ModelViewSet):

    queryset = LoanApplication.objects.select_related(
        "tenant", "branch", "customer", "product"
    )
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "tenant", "branch", "product", "income_type"]
    search_fields = [
        "application_id",
        "first_name",
        "last_name",
        "mobile_no",
        "pan_number",
    ]
    ordering_fields = ["created_at", "requested_amount", "status"]
    ordering = ["-created_at"]

    # --------------------------------------------------------
    # CREATE LOAN APPLICATION
    # --------------------------------------------------------
    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant,
            created_by=self.request.user,
            status="NEW",
        )

    # --------------------------------------------------------
    # RUN UNDERWRITING (RULE ENGINE)
    # --------------------------------------------------------
    @action(detail=True, methods=["post"], url_path="run-underwriting")
    def run_underwriting(self, request, pk=None):

        application = self.get_object()

        if application.status != "DOC_UPLOAD":
            return Response(
                {"detail": "Loan must be in DOC_UPLOAD stage"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mortgage validation
        if application.is_mortgage_loan():
            if not hasattr(application, "property_detail"):
                return Response(
                    {"detail": "Property details missing for Mortgage Loan"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        engine = RuleEngine(application)

        with transaction.atomic():

            # 1️⃣ Knockout checks
            knockout = engine.run_knockout_checks()
            if not knockout["is_eligible"]:
                application.status = "REJECTED"
                application.remarks = knockout["rejection_reason"]
                application.save(update_fields=["status", "remarks"])
                return Response(knockout, status=400)

            # 2️⃣ Underwriting calculations
            underwriting = engine.calculate_underwriting()

            credit, _ = CreditAssessment.objects.get_or_create(
                application=application
            )

            credit.status = (
                "SYSTEM_APPROVED"
                if underwriting["system_decision"] == "APPROVE"
                else "SYSTEM_REJECTED"
            )
            credit.remarks = "Rule engine underwriting"
            credit.save(update_fields=["status", "remarks"])

            application.foir_percentage = underwriting.get("foir_percentage")
            application.net_cash_flow = underwriting.get("net_cash_flow")
            application.status = "UNDERWRITING"

            application.save(
                update_fields=["foir_percentage", "net_cash_flow", "status"]
            )

        return Response(
            {
                "message": "Underwriting completed successfully",
                "underwriting": underwriting,
            },
            status=status.HTTP_200_OK,
        )

    # --------------------------------------------------------
    # SANCTION LOAN
    # --------------------------------------------------------
    @action(detail=True, methods=["post"], url_path="generate-sanction")
    def generate_sanction(self, request, pk=None):

        application = self.get_object()

        if application.status != "UNDERWRITING":
            return Response(
                {"detail": "Loan not ready for sanction"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sanction_doc = SmartVerificationService.generate_sanction_letter_pdf(
            application
        )

        application.status = "SANCTIONED"
        application.save(update_fields=["status"])

        return Response(
            {
                "message": "Loan sanctioned successfully",
                "sanction_letter": sanction_doc,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# KYC MODULE
# ============================================================
class KYCDetailViewSet(viewsets.ModelViewSet):

    queryset = KYCDetail.objects.select_related("loan_application")
    serializer_class = KYCDetailSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["loan_application", "kyc_type", "status"]


# ============================================================
# CREDIT ASSESSMENT (READ ONLY)
# ============================================================
class CreditAssessmentViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = CreditAssessment.objects.select_related("application")
    serializer_class = CreditAssessmentSerializer
    permission_classes = [IsAuthenticated]


# ============================================================
# PROPERTY DETAIL (MORTGAGE ONLY)
# ============================================================
class PropertyDetailViewSet(viewsets.ModelViewSet):

    queryset = PropertyDetail.objects.select_related("loan_application")
    serializer_class = PropertyDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(
            loan_application__product__name__iexact="Mortgage Loan"
        )
