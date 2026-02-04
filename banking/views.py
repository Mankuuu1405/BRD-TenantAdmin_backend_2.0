from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from banking.models import Mandate
from los.models import BankDetail
from .serializers import (
    BankingDashboardSerializer,
    BankAccountOnlySerializer,
)


class BankingDashboardViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BankingDashboardSerializer

    queryset = (
        Mandate.objects
        .select_related(
            "loan_application",
            "loan_application__customer",
            "loan_application__bank_detail",
        )
    )

class BankAccountListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bank_details = BankDetail.objects.all()
        serializer = BankAccountOnlySerializer(bank_details, many=True)
        return Response(serializer.data)
