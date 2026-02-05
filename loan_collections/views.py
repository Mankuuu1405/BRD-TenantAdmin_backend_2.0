from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Delinquency


class CollectionStatsAPIView(APIView):
    def get(self, request):
        return Response({
            "total_accounts": Delinquency.objects.count(),
            "npa_accounts": Delinquency.objects.filter(bucket="90+").count(),
        })


class OverdueLoansAPIView(APIView):
    def get(self, request):
        qs = Delinquency.objects.all().values(
            "loan_account_id",
            "borrower_name",
            "dpd",
            "overdue_amount",
            "bucket",
        )
        return Response(list(qs))
