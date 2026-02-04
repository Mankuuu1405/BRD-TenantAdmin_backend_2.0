from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, time
import calendar


# =====================================================
# 1. Financial Year
# =====================================================
class FinancialYear(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="inactive"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def clean(self):
        if not (self.start_date.month == 4 and self.start_date.day == 1):
            raise ValidationError("Financial year must start on April 1")
        if not (self.end_date.month == 3 and self.end_date.day == 31):
            raise ValidationError("Financial year must end on March 31")

    def save(self, *args, **kwargs):
        self.name = f"FY {self.start_date.year}-{str(self.end_date.year)[-2:]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =====================================================
# 2. Assessment Year (Linked to Financial Year)
# =====================================================
class AssessmentYear(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    financial_year = models.OneToOneField(
        FinancialYear,
        on_delete=models.CASCADE,
        related_name="assessment_year"
    )

    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="inactive"
    )

    # =============================
    # Configuration Settings
    # =============================
    financial_eligibility_years = models.PositiveIntegerField(default=3)
    document_compliance_required = models.BooleanField(default=True)
    credit_assessment_enabled = models.BooleanField(default=True)
    itr_years_required = models.PositiveIntegerField(default=3)
    loan_type_specific = models.BooleanField(default=False)
    borrower_type_specific = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Start date must be 1st April of next year after FY
        if not (self.start_date.month == 4 and self.start_date.day == 1):
            raise ValidationError("Assessment Year must start on April 1")

        # End date must be 31st March
        if not (self.end_date.month == 3 and self.end_date.day == 31):
            raise ValidationError("Assessment Year must end on March 31")

    def save(self, *args, **kwargs):
        fy = self.financial_year

        # Auto-calculate dates
        self.start_date = date(fy.start_date.year + 1, 4, 1)
        self.end_date = date(fy.start_date.year + 2, 3, 31)

        # Auto-generate AY name
        self.name = f"AY {fy.start_date.year + 1}-{str(fy.start_date.year + 2)[-2:]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



# =====================================================
# 3. Reporting Period
# =====================================================
class ReportingPeriod(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")

    def __str__(self):
        return self.name


# =====================================================
# 4. Holidays
# =====================================================
class Holiday(models.Model):
    date = models.DateField(unique=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} ({self.date})"


# =====================================================
# 5. Working Days
# =====================================================
class WorkingDay(models.Model):
    DAY_CHOICES = (
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    )

    day = models.CharField(max_length=3, choices=DAY_CHOICES, unique=True)
    is_working = models.BooleanField(default=True)

    def __str__(self):
        return dict(self.DAY_CHOICES)[self.day]


# =====================================================
# 6. Working Hours
# =====================================================
class WorkingHour(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


# =====================================================
# 7. Overtime
# =====================================================
class Overtime(models.Model):
    enabled = models.BooleanField(default=False)
    rate_multiplier = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Example: 1.5x, 2.0x"
    )

    def __str__(self):
        return f"Enabled: {self.enabled}, Rate: {self.rate_multiplier}x"
