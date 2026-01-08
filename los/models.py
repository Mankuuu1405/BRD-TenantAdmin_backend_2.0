import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from adminpanel.models import LoanProduct


# ============================================
# HELPER FUNCTION FOR UNIQUE APPLICATION NUMBER
# ============================================
def generate_application_number():
    """Generates a unique application number"""
    return str(uuid.uuid4())


# ============================================
# LOAN APPLICATION
# ============================================
class LoanApplication(models.Model):
    # -------------------------
    # STATUS CHOICES
    # -------------------------
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('KNOCKOUT_PENDING', 'Knockout Checks'),
        ('DOC_UPLOAD', 'Document Upload'),
        ('UNDERWRITING', 'Underwriting'),
        ('HOLD', 'On Hold'),
        ('SANCTIONED', 'Sanctioned'),
        ('PRE_DISBURSEMENT', 'Pre Disbursement'),
        ('DISBURSED', 'Disbursed'),
        ('REJECTED', 'Rejected'),
        ('CLOSED', 'Closed'),
    )

    BORROWER_TYPE_CHOICES = (
        ("INDIVIDUAL", "Individual"),
        ("PARTNERSHIP", "Partnership Firm"),
        ("CORPORATE", "Corporate"),
    )

    INCOME_TYPE_CHOICES = (
        ("SALARIED", "Salaried"),
        ("SELF_EMPLOYED", "Self Employed"),
    )

    # -------------------------
    # IDENTIFIERS
    # -------------------------
    application_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    application_number = models.CharField(
        max_length=50,
        unique=True,
        default=generate_application_number,  # callable for unique value
        editable=False
    )

    # -------------------------
    # RELATIONSHIPS
    # -------------------------
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    branch = models.ForeignKey('tenants.Branch', on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey('crm.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey(LoanProduct, on_delete=models.PROTECT)

    # -------------------------
    # LOAN DETAILS
    # -------------------------
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='NEW')
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    requested_tenure = models.IntegerField(help_text="Months")
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # -------------------------
    # BORROWER INFO
    # -------------------------
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField()
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    pan_number = models.CharField(max_length=10)
    aadhaar_number = models.CharField(max_length=12, null=True, blank=True)
    borrower_type = models.CharField(max_length=20, choices=BORROWER_TYPE_CHOICES)
    income_type = models.CharField(max_length=20, choices=INCOME_TYPE_CHOICES)
    employer_name = models.CharField(max_length=255, null=True, blank=True)
    business_name = models.CharField(max_length=255, null=True, blank=True)

    # -------------------------
    # ADDRESS INFO
    # -------------------------
    res_address_line1 = models.CharField(max_length=255)
    res_city = models.CharField(max_length=100)
    res_state = models.CharField(max_length=100)
    res_pincode = models.CharField(max_length=6)
    office_address_line1 = models.CharField(max_length=255, blank=True)
    office_city = models.CharField(max_length=100, blank=True)
    office_pincode = models.CharField(max_length=6, blank=True)

    # -------------------------
    # SYSTEM INFO
    # -------------------------
    remarks = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "loan_applications"
        ordering = ['-created_at']

    # -------------------------
    # VALIDATIONS
    # -------------------------
    def clean(self):
        if self.income_type == 'SALARIED' and not self.employer_name:
            raise ValidationError("Employer name is required for salaried applicants.")
        if self.income_type == 'SELF_EMPLOYED' and not self.business_name:
            raise ValidationError("Business name is required for self-employed applicants.")

    def is_mortgage_loan(self):
        return self.product.loan_type == "MORTGAGE"


# ============================================
# BANK DETAIL
# ============================================
class BankDetail(models.Model):
    loan_application = models.OneToOneField(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name='bank_detail'
    )

    account_number = models.CharField(max_length=20, default='0000000000')
    ifsc_code = models.CharField(max_length=11, default='UNKNOWNIFSC')
    bank_name = models.CharField(max_length=255, default='Unknown Bank')
    branch_name = models.CharField(max_length=255, null=True, blank=True)

    penny_drop_status = models.CharField(max_length=20, default='PENDING')
    enach_status = models.CharField(max_length=20, default='NOT_REGISTERED')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bank_details"

    def __str__(self):
        return f"{self.bank_name} - ****{self.account_number[-4:]}"


# ============================================
# KYC DETAIL
# ============================================
class KYCDetail(models.Model):
    KYC_TYPES = (
        ('PAN', 'PAN'),
        ('AADHAAR', 'Aadhaar'),
        ('BANK_STATEMENT', 'Bank Statement'),
        ('SALARY_SLIP', 'Salary Slip'),
        ('ITR', 'ITR'),
        ('GST', 'GST'),
        ('SALE_DEED', 'Sale Deed'),
        ('ENCUMBRANCE_CERT', 'Encumbrance Certificate'),
    )

    loan_application = models.ForeignKey(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    kyc_type = models.CharField(max_length=50, choices=KYC_TYPES)
    document_file = models.FileField(upload_to='kyc/')
    status = models.CharField(max_length=20, default='PENDING')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "kyc_details"


# ============================================
# PROPERTY DETAIL
# ============================================

class PropertyDetail(models.Model):

    PROPERTY_TYPE_CHOICES = [
        ('HOUSE', 'House'),
        ('FLAT', 'Flat / Apartment'),
        ('PLOT', 'Plot / Land'),
        ('VILLA', 'Villa'),
        ('COMMERCIAL', 'Commercial Property'),
    ]

    loan_application = models.OneToOneField(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name='property_detail'
    )

    property_type = models.CharField(
        max_length=30,
        choices=PROPERTY_TYPE_CHOICES
    )

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "property_details"



# ============================================
# CREDIT ASSESSMENT
# ============================================
class CreditAssessment(models.Model):
    DECISION_CHOICES = (
        ("SYSTEM_APPROVED", "System Approved"),
        ("SYSTEM_REJECTED", "System Rejected"),
        ("MANUAL_APPROVED", "Manual Approved"),
        ("MANUAL_REJECTED", "Manual Rejected"),
    )

    application = models.OneToOneField(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name="credit_assessment"
    )
    status = models.CharField(max_length=30, choices=DECISION_CHOICES)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "credit_assessments"

    def __str__(self):
        return f"{self.application.application_id} - {self.status}"


# ============================================
# MORTGAGE UNDERWRITING
# ============================================
class MortgageUnderwriting(models.Model):
    loan_application = models.OneToOneField(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name='mortgage_underwriting'
    )

    property_market_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ltv_on_property = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_eligible_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    approved_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mortgage_underwriting"

    def __str__(self):
        return f"Mortgage UW - {self.loan_application.application_id}"
