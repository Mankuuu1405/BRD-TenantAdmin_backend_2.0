from django.db import models


# 🔹 Base permission model (REUSABLE)
class BaseRule(models.Model):
    can_view = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True  # ❗ no table created for this


# 🔹 Access Rules
class AccessRule(BaseRule):
    def __str__(self):
        return f"AccessRule {self.id}"


# 🔹 Workflow Rules
class WorkflowRule(BaseRule):
    def __str__(self):
        return f"WorkflowRule {self.id}"


# 🔹 Validation Rules
class ValidationRule(BaseRule):
    def __str__(self):
        return f"ValidationRule {self.id}"


# 🔹 Assignment Rules
class AssignmentRule(BaseRule):
    def __str__(self):
        return f"AssignmentRule {self.id}"


# 🔹 Security Rules
class SecurityRule(BaseRule):
    def __str__(self):
        return f"SecurityRule {self.id}"
