from rest_framework.generics import ListAPIView
from .models import LoanAccount
from .serializers import LoanAccountListSerializer
class LoanAccountListAPIView(ListAPIView):
    queryset = LoanAccount.objects.select_related("disbursement")
    serializer_class = LoanAccountListSerializer
