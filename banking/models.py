from django.db import models
from los.models import LoanApplication

class Mandate(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )

    loan_application = models.OneToOneField(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name="mandate"
    )

    penny_drop_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    enach_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    failure_reason = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mandate - {self.loan_application.id}"
