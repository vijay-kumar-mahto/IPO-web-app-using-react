from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Company(models.Model):
    """Model representing a company that has an IPO."""
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255, null=False, blank=False)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['company_name']

    def __str__(self):
        return self.company_name


class IPO(models.Model):
    """Model representing an Initial Public Offering."""
    STATUS_CHOICES = (
        ('Upcoming', 'Upcoming'),
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Listed', 'Listed'),
    )

    ipo_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ipos')
    price_band = models.CharField(max_length=50, null=True, blank=True)
    open_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    issue_size = models.CharField(max_length=100, null=True, blank=True)
    issue_type = models.CharField(max_length=50, null=True, blank=True)
    listing_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Upcoming')
    ipo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    listing_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    listing_gain = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                      validators=[MinValueValidator(-100), MaxValueValidator(1000)])
    current_market_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_return = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                        validators=[MinValueValidator(-100), MaxValueValidator(1000)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'IPO'
        verbose_name_plural = 'IPOs'
        ordering = ['-open_date']

    def __str__(self):
        return f"{self.company.company_name} IPO"


class Document(models.Model):
    """Model representing IPO-related documents like RHP and DRHP."""
    document_id = models.AutoField(primary_key=True)
    ipo = models.ForeignKey(IPO, on_delete=models.CASCADE, related_name='documents')
    rhp_pdf = models.FileField(upload_to='ipo_documents/rhp/', null=True, blank=True)
    drhp_pdf = models.FileField(upload_to='ipo_documents/drhp/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f"Documents for {self.ipo.company.company_name} IPO"