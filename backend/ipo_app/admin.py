from django.contrib import admin
from .models import Company, IPO, Document


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'company_name', 'created_at', 'updated_at')
    search_fields = ('company_name',)
    list_filter = ('created_at',)
    ordering = ('company_name',)


@admin.register(IPO)
class IPOAdmin(admin.ModelAdmin):
    list_display = ('ipo_id', 'company', 'price_band', 'open_date', 'close_date', 
                   'status', 'listing_date', 'ipo_price', 'listing_gain', 'current_return')
    list_filter = ('status', 'open_date', 'listing_date')
    search_fields = ('company__company_name', 'issue_type')
    date_hierarchy = 'open_date'
    inlines = [DocumentInline]
    list_editable = ('status',)
    fieldsets = (
        ('Company Information', {
            'fields': ('company',)
        }),
        ('IPO Details', {
            'fields': ('price_band', 'issue_size', 'issue_type', 'status')
        }),
        ('Important Dates', {
            'fields': ('open_date', 'close_date', 'listing_date')
        }),
        ('Financial Information', {
            'fields': ('ipo_price', 'listing_price', 'listing_gain', 'current_market_price', 'current_return')
        }),
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'ipo', 'has_rhp', 'has_drhp', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('ipo__company__company_name',)
    
    def has_rhp(self, obj):
        return bool(obj.rhp_pdf)
    has_rhp.boolean = True
    
    def has_drhp(self, obj):
        return bool(obj.drhp_pdf)
    has_drhp.boolean = True