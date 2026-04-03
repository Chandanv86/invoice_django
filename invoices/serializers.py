from rest_framework import serializers
from .models import Salesperson, Party, ProformaInvoice, InvoiceItem, CompanyProfile, PriceListEntry, MasterItem

class SalespersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salesperson
        fields = '__all__'

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        read_only_fields = ('proforma',) # Will be set by ProformaSerializer

class ProformaInvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, required=False)

    class Meta:
        model = ProformaInvoice
        fields = '__all__'
    
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        proforma = ProformaInvoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(proforma=proforma, **item_data)
        return proforma

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        
        # Update Proforma fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update items
        if items_data is not None:
            # Delete existing items not in request (naive approach, can optimize later)
            instance.items.all().delete()
            for item_data in items_data:
                InvoiceItem.objects.create(proforma=instance, **item_data)
                
        return instance

class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = '__all__'

class PriceListEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceListEntry
        fields = '__all__'

class MasterItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterItem
        fields = '__all__'
