from rest_framework import generics, permissions
from .models import CreditScoreRule, NegativeArea
from .serializers import CreditScoreRuleSerializer, NegativeAreaSerializer

class CreditScoreRuleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CreditScoreRuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CreditScoreRule.objects.filter(
            tenant=self.request.user.tenant,
            employment_type=self.request.query_params.get('type', 'SALARIED')
        )

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)
class NegativeAreaListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = NegativeAreaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NegativeArea.objects.filter(
            tenant=self.request.user.tenant,
            is_active=True
        )

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)
