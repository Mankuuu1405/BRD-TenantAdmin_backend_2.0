from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Disbursement
from .serializers import DisbursementQueueSerializer


class DisbursementQueueAPIView(ListAPIView):
    serializer_class = DisbursementQueueSerializer

    def get_queryset(self):
        return Disbursement.objects.all()


class DisburseLoanAPIView(APIView):
    def post(self, request, application_id):
        try:
            disbursement = Disbursement.objects.get(
                loan_application__id=application_id
            )

            # mock success
            disbursement.penny_drop_status = "SUCCESS"
            disbursement.enach_status = "SUCCESS"
            disbursement.save()

            return Response(
                {"message": "Disbursement successful"},
                status=status.HTTP_200_OK
            )

        except Disbursement.DoesNotExist:
            return Response(
                {"error": "Disbursement not found"},
                status=status.HTTP_404_NOT_FOUND
            )
