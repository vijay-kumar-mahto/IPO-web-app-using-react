from django.db import models


class Broker(models.Model):
    """Model representing a broker that offers IPO services."""
    broker_id = models.AutoField(primary_key=True)
    broker_name = models.CharField(max_length=255, null=False, blank=False)
    broker_logo = models.ImageField(upload_to='broker_logos/', null=True, blank=True)
    website_url = models.URLField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    min_account_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    account_opening_link = models.URLField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Broker'
        verbose_name_plural = 'Brokers'
        ordering = ['broker_name']

    def __str__(self):
        return self.broker_name