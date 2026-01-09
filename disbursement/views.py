from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from los.models import LoanApplication


# ============================
# DISBURSEMENT QUEUE (GET)
# ============================
class DisbursementQueueAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        applications = LoanApplication.objects.filter(
            status='PRE_DISBURSEMENT'
        )

        data = []
        for app in applications:
            data.append({
                "id": app.id,
                "applicant_name": f"{app.first_name} {app.last_name}",
                "sanctioned_amount": app.requested_amount,
            })

        return Response(data)


# ============================
# DISBURSE LOAN (POST)
# ============================
class DisburseLoanAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, application_id):
        loan = get_object_or_404(LoanApplication, id=application_id)

        # Safety check
        if loan.status != 'PRE_DISBURSEMENT':
            return Response(
                {"error": "Loan is not ready for disbursement"},
                status=400
            )

        loan.status = 'DISBURSED'
        loan.save()

        return Response({"message": "Loan disbursed successfully"})
