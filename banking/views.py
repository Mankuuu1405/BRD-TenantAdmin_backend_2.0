from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from los.models import LoanApplication, BankDetail
from .serializers import BankingDashboardSerializer, BankAccountOnlySerializer


class BankingDashboardViewSet(ReadOnlyModelViewSet):
    """
    Banking module is READ ONLY.
    Loan + bank data comes from LOS.
    """
    permission_classes = [IsAuthenticated]

    queryset = (
    LoanApplication.objects
    .select_related("customer")
    .select_related("bank_detail")
)

    serializer_class = BankingDashboardSerializer


class BankAccountListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bank_details = BankDetail.objects.all()
        serializer = BankAccountOnlySerializer(bank_details, many=True)
        return Response(serializer.data)

