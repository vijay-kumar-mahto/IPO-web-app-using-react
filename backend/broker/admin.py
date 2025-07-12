from django.contrib import admin
from .models import Broker


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('broker_id', 'broker_name', 'website_url', 'min_account_size', 'created_at')
    search_fields = ('broker_name', 'description')
    list_filter = ('created_at',)
    ordering = ('broker_name',)