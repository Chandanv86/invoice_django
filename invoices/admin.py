from django.contrib import admin
from .models import Salesperson, Party, ProformaInvoice, InvoiceItem, CompanyProfile, PriceListEntry, MasterItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

@admin.register(ProformaInvoice)
class ProformaInvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'partyId', 'spId', 'grandTotal')
    inlines = [InvoiceItemInline]
    search_fields = ('number',)
    list_filter = ('date', 'spId')

@admin.register(Salesperson)
class SalespersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'spId')
    list_filter = ('spId',)
    search_fields = ('name', 'city')

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone')

@admin.register(PriceListEntry)
class PriceListEntryAdmin(admin.ModelAdmin):
    list_display = ('itemName', 'rate')
    search_fields = ('itemName',)

@admin.register(MasterItem)
class MasterItemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
