from django.db import models
from django.utils import timezone
import uuid

class Salesperson(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class Party(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4, editable=False)
    spId = models.ForeignKey(Salesperson, on_delete=models.CASCADE, related_name='parties', db_column='spId')
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    gstin = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    pin = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class ProformaInvoice(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    validTill = models.DateField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    discount = models.FloatField(default=0)
    showDiscInPDF = models.BooleanField(default=False)
    freight = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    gstAmt = models.FloatField(default=0)
    grandTotal = models.FloatField(default=0)
    
    partyId = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='proformas', db_column='partyId')
    spId = models.ForeignKey(Salesperson, on_delete=models.CASCADE, related_name='proformas', db_column='spId')
    
    # Store shipTo as JSON
    shipTo = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.number

class InvoiceItem(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4, editable=False)
    proforma = models.ForeignKey(ProformaInvoice, on_delete=models.CASCADE, related_name='items')
    itemName = models.CharField(max_length=255)
    qty = models.FloatField()
    rate = models.FloatField() # This usually represents List Rate
    listRate = models.FloatField()
    netRate = models.FloatField()
    unit = models.CharField(max_length=50)
    amount = models.FloatField()
    disc = models.FloatField(default=0)
    itemDisc = models.FloatField(default=0) # Same as disc from data
    narration = models.CharField(max_length=255, blank=True, null=True)
    manualNet = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.itemName} - {self.qty}"

class CompanyProfile(models.Model):
    name = models.CharField(max_length=255, default='ATUL INDUSTRIES')
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pin = models.CharField(max_length=20, blank=True, null=True)
    gstin = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    bank = models.CharField(max_length=255, blank=True, null=True)
    account = models.CharField(max_length=100, blank=True, null=True)
    ifsc = models.CharField(max_length=50, blank=True, null=True)
    branch = models.CharField(max_length=255, blank=True, null=True)
    defaultTerms = models.TextField(blank=True, null=True)
    pipePacking = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

class PriceListEntry(models.Model):
    itemName = models.CharField(max_length=255, unique=True)
    rate = models.FloatField()

    def __str__(self):
        return f"{self.itemName}: {self.rate}"

class MasterItem(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
