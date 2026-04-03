import json

from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

from .models import (
    Salesperson, Party, ProformaInvoice, InvoiceItem,
    CompanyProfile, PriceListEntry, MasterItem
)
from .serializers import (
    SalespersonSerializer, PartySerializer, ProformaInvoiceSerializer, 
    CompanyProfileSerializer, PriceListEntrySerializer, MasterItemSerializer
)

@api_view(['POST'])
def sync_db(request):
    """Fallback endpoint to sync the entire DB from frontend."""
    data = request.data
    
    # Simple clear and recreate for MVP
    Salesperson.objects.all().delete()
    Party.objects.all().delete()
    ProformaInvoice.objects.all().delete()
    InvoiceItem.objects.all().delete()
    
    # 1. Salesperson
    for sp_data in data.get('sp', []):
        Salesperson.objects.create(
            id=sp_data['id'],
            name=sp_data['name'],
            phone=sp_data.get('phone', ''),
            email=sp_data.get('email', ''),
        )

    # 2. Party
    for p_data in data.get('parties', []):
        sp = Salesperson.objects.get(id=p_data['spId'])
        Party.objects.create(
            id=p_data['id'],
            spId=sp,
            name=p_data['name'],
            contact=p_data.get('contact', ''),
            city=p_data.get('city', ''),
            state=p_data.get('state', ''),
            gstin=p_data.get('gstin', ''),
            address=p_data.get('address', ''),
            phone=p_data.get('phone', ''),
            email=p_data.get('email', ''),
            pin=p_data.get('pin', '')
        )
    
    # 3. Proformas & Items
    for pf_data in data.get('proformas', []):
        party = Party.objects.get(id=pf_data['partyId'])
        sp = Salesperson.objects.get(id=pf_data['spId'])
        
        pf = ProformaInvoice.objects.create(
            id=pf_data['id'],
            partyId=party,
            spId=sp,
            number=pf_data['number'],
            date=pf_data['date'],
            validTill=pf_data.get('validTill') or None,
            subject=pf_data.get('subject', ''),
            notes=pf_data.get('notes', ''),
            discount=pf_data.get('discount', 0),
            showDiscInPDF=pf_data.get('showDiscInPDF', False),
            freight=pf_data.get('freight', 0),
            subtotal=pf_data.get('subtotal', 0),
            gstAmt=pf_data.get('gstAmt', 0),
            grandTotal=pf_data.get('grandTotal', 0),
            shipTo=pf_data.get('shipTo')
        )

        for item_data in pf_data.get('items', []):
            InvoiceItem.objects.create(
                proforma=pf,
                id=item_data['id'],
                itemName=item_data['itemName'],
                qty=item_data['qty'],
                rate=item_data['rate'],
                listRate=item_data.get('listRate', item_data['rate']),
                netRate=item_data.get('netRate', item_data['rate']),
                unit=item_data['unit'],
                amount=item_data['amount'],
                disc=item_data['disc'],
                narration=item_data.get('narration', '')
            )

    return Response({"status": "success"})

# --- Template Views ---
def home_view(request):
    """Serve the main SPA application."""
    sp_data = list(Salesperson.objects.values())
    party_data = list(Party.objects.values())
    proforma_data = list(ProformaInvoice.objects.values())
    for pf in proforma_data:
        # Fetch items
        pf['items'] = list(InvoiceItem.objects.filter(proforma_id=pf['id']).values())
        if pf.get('date'):
            pf['date'] = str(pf['date'])
        if pf.get('validTill'):
            pf['validTill'] = str(pf['validTill'])

    db = {
        'sp': sp_data,
        'parties': party_data,
        'proformas': proforma_data
    }
    
    try:
        co = CompanyProfile.get_solo()
        co_data = CompanyProfileSerializer(co).data
    except Exception:
        co_data = {}

    pl_entries = list(PriceListEntry.objects.values('itemName', 'rate'))
    pl_data = {entry['itemName']: entry['rate'] for entry in pl_entries}
    
    master_items = list(MasterItem.objects.values_list('name', flat=True))

    context = {
        'db_json': json.dumps(db, cls=DjangoJSONEncoder),
        'co_json': json.dumps(co_data, cls=DjangoJSONEncoder),
        'pl_json': json.dumps(pl_data, cls=DjangoJSONEncoder),
        'master_items_json': json.dumps(master_items, cls=DjangoJSONEncoder),
    }

    return render(request, 'invoices/base.html', context)

# --- API ViewSets ---

class SalespersonViewSet(viewsets.ModelViewSet):
    queryset = Salesperson.objects.all()
    serializer_class = SalespersonSerializer

class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    @action(detail=False, methods=['get'])
    def by_salesperson(self, request):
        sp_id = request.query_params.get('spId')
        if sp_id:
            queryset = self.queryset.filter(spId=sp_id)
        else:
            queryset = self.queryset.none()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProformaInvoiceViewSet(viewsets.ModelViewSet):
    queryset = ProformaInvoice.objects.all().order_by('-date')
    serializer_class = ProformaInvoiceSerializer
    
    @action(detail=False, methods=['get'])
    def by_party(self, request):
        party_id = request.query_params.get('partyId')
        if party_id:
            queryset = self.queryset.filter(partyId=party_id)
        else:
            queryset = self.queryset.none()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CompanyProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        profile = CompanyProfile.get_solo()
        serializer = CompanyProfileSerializer(profile)
        return Response(serializer.data)
        
    def create(self, request):
        profile = CompanyProfile.get_solo()
        serializer = CompanyProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class PriceListEntryViewSet(viewsets.ModelViewSet):
    queryset = PriceListEntry.objects.all()
    serializer_class = PriceListEntrySerializer

class MasterItemViewSet(viewsets.ModelViewSet):
    queryset = MasterItem.objects.all()
    serializer_class = MasterItemSerializer
