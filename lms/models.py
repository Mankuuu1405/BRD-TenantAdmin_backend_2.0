from django.db import models
from disbursement.models import Disbursement


class LoanStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    CLOSED = "CLOSED", "Closed"


class ActionType(models.TextChoices):
    DEACTIVE = "DEACTIVE", "Deactive"
    TAKEN = "TAKEN", "Taken"


class LoanAccount(models.Model):
    # Link to the Disbursement model
    disbursement = models.OneToOneField(
        Disbursement, 
        on_delete=models.CASCADE,  # or PROTECT if you don't want deletion
        related_name="loan_account"
    )
    
    principal = models.DecimalField(max_digits=14, decimal_places=2)
    outstanding_principal = models.DecimalField(max_digits=14, decimal_places=2)
    
    status = models.CharField(
        max_length=50,
        choices=LoanStatus.choices,
        default=LoanStatus.ACTIVE
    )
    action = models.CharField(
        max_length=50,
        choices=LoanStatus.choices,
        default=LoanStatus.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"LoanAccount({self.disbursement.id}) - {self.status}"
