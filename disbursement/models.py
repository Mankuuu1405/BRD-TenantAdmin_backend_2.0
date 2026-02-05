from django.db import models
from los.models import LoanApplication

class Disbursement(models.Model):
    loan_application = models.OneToOneField(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name='disbursement'
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    penny_drop_status = models.CharField(
        max_length=10,
        choices=[
            ('PENDING', 'Pending'),
            ('SUCCESS', 'Success'),
            ('FAILED', 'Failed'),
        ],
        default='PENDING'
    )

    enach_status = models.CharField(
        max_length=10,
        choices=[
            ('PENDING', 'Pending'),
            ('SUCCESS', 'Success'),
            ('FAILED', 'Failed'),
        ],
        default='PENDING'
    )

    failure_reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Disbursement - {self.loan_application.application_id}"
