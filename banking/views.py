from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Mandate
from .serializers import MandateSerializer


class MandateViewSet(ReadOnlyModelViewSet):
    queryset = Mandate.objects.all() 
    serializer_class = MandateSerializer

    def get_queryset(self):
        return (
            Mandate.objects
            .select_related(
                "loan_application",
                "loan_application__customer"
            )
            .order_by("-created_at")
        )
