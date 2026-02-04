from rest_framework import serializers
from .models import (
    AccessRule,
    WorkflowRule,
    ValidationRule,
    AssignmentRule,
    SecurityRule,
)


class BaseRuleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"


class AccessRuleSerializer(BaseRuleSerializer):
    class Meta(BaseRuleSerializer.Meta):
        model = AccessRule


class WorkflowRuleSerializer(BaseRuleSerializer):
    class Meta(BaseRuleSerializer.Meta):
        model = WorkflowRule


class ValidationRuleSerializer(BaseRuleSerializer):
    class Meta(BaseRuleSerializer.Meta):
        model = ValidationRule


class AssignmentRuleSerializer(BaseRuleSerializer):
    class Meta(BaseRuleSerializer.Meta):
        model = AssignmentRule


class SecurityRuleSerializer(BaseRuleSerializer):
    class Meta(BaseRuleSerializer.Meta):
        model = SecurityRule
