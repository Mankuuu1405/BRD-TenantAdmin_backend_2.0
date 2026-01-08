# models.py
from django.db import models
from django.utils import timezone

class Mandate(models.Model):

    class PennyDropStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    class ENachStatus(models.TextChoices):
        NOT_REGISTERED = "NOT_REGISTERED", "Not Registered"
        REGISTERED = "REGISTERED", "Registered"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    loan_application = models.OneToOneField(
        "los.LoanApplication",
        on_delete=models.CASCADE,
        related_name="mandate"
    )

    penny_drop_status = models.CharField(
        max_length=20,
        choices=PennyDropStatus.choices,
        default=PennyDropStatus.PENDING
    )

    enach_status = models.CharField(
        max_length=20,
        choices=ENachStatus.choices,
        default=ENachStatus.NOT_REGISTERED
    )

    verified_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)  # ✅ MIGRATION SAFE
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mandate - LoanApp {self.loan_application_id}"
