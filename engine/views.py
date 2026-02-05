from rest_framework.viewsets import ModelViewSet
from .models import (
    AccessRule,
    WorkflowRule,
    ValidationRule,
    AssignmentRule,
    SecurityRule,
)
from .serializers import (
    AccessRuleSerializer,
    WorkflowRuleSerializer,
    ValidationRuleSerializer,
    AssignmentRuleSerializer,
    SecurityRuleSerializer,
)


class AccessRuleViewSet(ModelViewSet):
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer


class WorkflowRuleViewSet(ModelViewSet):
    queryset = WorkflowRule.objects.all()
    serializer_class = WorkflowRuleSerializer


class ValidationRuleViewSet(ModelViewSet):
    queryset = ValidationRule.objects.all()
    serializer_class = ValidationRuleSerializer


class AssignmentRuleViewSet(ModelViewSet):
    queryset = AssignmentRule.objects.all()
    serializer_class = AssignmentRuleSerializer


class SecurityRuleViewSet(ModelViewSet):
    queryset = SecurityRule.objects.all()
    serializer_class = SecurityRuleSerializer
