from django.db import models


class Delinquency(models.Model):
    """
    Loan Account comes from LMS (Disbursement ID)
    """

    ACTION_CHOICES = (
        ("CALL", "Call Borrower"),
        ("VISIT", "Field Visit"),
        ("LEGAL", "Legal Notice"),
        ("SETTLED", "Settled"),
    )

    BUCKET_CHOICES = (
        ("0-30", "0-30 DPD"),
        ("31-60", "31-60 DPD"),
        ("61-90", "61-90 DPD"),
        ("90+", "90+ DPD (NPA)"),
    )

    # LMS reference (NO FK)
    loan_account_id = models.CharField(max_length=100, db_index=True)  # Disbursement ID
    borrower_name = models.CharField(max_length=255)

    dpd = models.PositiveIntegerField()
    overdue_amount = models.DecimalField(max_digits=14, decimal_places=2)
    bucket = models.CharField(max_length=10, choices=BUCKET_CHOICES)

    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["loan_account_id"]),
            models.Index(fields=["bucket"]),
        ]

    def __str__(self):
        return f"{self.loan_account_id} | {self.bucket}"
