from django.contrib import admin
from .models import (
    AccessRule,
    WorkflowRule,
    ValidationRule,
    AssignmentRule,
    SecurityRule,
)


class BaseRuleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "can_view",
        "can_add",
        "can_edit",
        "can_delete",
        "created_at",
    )
    list_filter = (
        "can_view",
        "can_add",
        "can_edit",
        "can_delete",
    )
    readonly_fields = ("created_at",)


@admin.register(AccessRule)
class AccessRuleAdmin(BaseRuleAdmin):
    pass


@admin.register(WorkflowRule)
class WorkflowRuleAdmin(BaseRuleAdmin):
    pass


@admin.register(ValidationRule)
class ValidationRuleAdmin(BaseRuleAdmin):
    pass


@admin.register(AssignmentRule)
class AssignmentRuleAdmin(BaseRuleAdmin):
    pass


@admin.register(SecurityRule)
class SecurityRuleAdmin(BaseRuleAdmin):
    pass
