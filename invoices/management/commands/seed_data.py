from django.core.management.base import BaseCommand
from invoices.models import Salesperson, Party, ProformaInvoice, InvoiceItem, CompanyProfile, PriceListEntry, MasterItem
from django.utils.dateparse import parse_date

class Command(BaseCommand):
    help = 'Seeds the database with initial proforma invoice data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Clear existing data
        Salesperson.objects.all().delete()
        Party.objects.all().delete()
        ProformaInvoice.objects.all().delete()
        InvoiceItem.objects.all().delete()
        PriceListEntry.objects.all().delete()
        MasterItem.objects.all().delete()

        SEED = {
            "sp": [
                {"id": "3d606b0f", "name": "Alok Singh", "phone": "9661510467", "email": "alok@atulpipes.com"}
            ],
            "parties": [
                {"id": "53c94d3e", "spId": "3d606b0f", "name": "Ambuja Trading", "city": "Patna", "state": "Bihar", "gstin": "", "address": "Patna, Bihar 800016", "phone": "", "email": ""},
                {"id": "36cedc0c", "spId": "3d606b0f", "name": "B Rai & Company", "city": "M/S B. Rai & Company", "state": "", "gstin": "", "address": "M/S B. Rai & Company", "phone": "", "email": ""},
                {"id": "19ad8fdf", "spId": "3d606b0f", "name": "Milan Electrical", "city": "Patna", "state": "", "gstin": "", "address": "Patna, Bihar- 800016", "phone": "", "email": ""},
                {"id": "a8012e67", "spId": "3d606b0f", "name": "Om Sai", "city": "Patna", "state": "", "gstin": "", "address": "Patna", "phone": "", "email": ""},
                {"id": "8e021ce2", "spId": "3d606b0f", "name": "SKS", "city": "M/s SKS Construction Company", "state": "", "gstin": "", "address": "M/s SKS Construction Company", "phone": "", "email": ""},
                {"id": "5810d751", "spId": "3d606b0f", "name": "Thakur Enterprises", "city": "M/s Thakur Enterprises", "state": "", "gstin": "", "address": "M/s Thakur Enterprises", "phone": "", "email": ""},
                {"id": "cafeeaf4", "spId": "3d606b0f", "name": "Sarang Electric", "city": "M/s Sarang Electric", "state": "", "gstin": "", "address": "M/s Sarang Electric", "phone": "", "email": ""}
            ],
            "proformas": [
                {
                    "id": "8b8dcfa0", "number": "PI-AL-2512-01", "date": "2025-12-05", "validTill": "", 
                    "subject": "Supply of PVC Conduit Pipes & Fittings", 
                    "notes": "Price: Ex Unit\nPayment: Advance\nFreight: FoR\nDelivery: 2-3 Days\nValidity: 7 Days\nContact: Alok Singh (9661510467)", 
                    "discount": 0, "showDiscInPDF": False, 
                    "items": [
                        {"itemName": "PVC Conduit Pipe 20mm Light", "qty": 20.0, "rate": 1003.2, "listRate": 1003.2, "netRate": 1003.2, "unit": "Bundle", "amount": 20064.0, "disc": 0, "narration": "", "id": "ee613032"}
                    ], 
                    "subtotal": 20064.0, "gstAmt": 3611.52, "grandTotal": 23675.52, "partyId": "53c94d3e", "spId": "3d606b0f", "shipTo": None
                }
            ]
        }

        ITEMS = [
            'PVC Conduit Pipe 25mm Heavy (2mm Thick)', 'PVC Conduit Pipe 25mm Heavy',
            'PVC Conduit Pipe 25mm Medium (1.6mm Thick)', 'PVC Conduit Pipe 25mm Medium',
            'PVC Conduit Pipe 20mm Heavy (2mm Thick)', 'PVC Conduit Pipe 20mm Heavy',
            'PVC Conduit Pipe 20mm Medium (1.6mm Thick)', 'PVC Conduit Pipe 20mm Medium',
            'PVC Bend 20mm Medium', 'PVC Bend 20mm Heavy', 'PVC Bend 20mm Heavy (2mm Thick)',
            'PVC Bend 25mm Medium', 'PVC Bend 25mm Heavy', 'PVC Bend 25mm Heavy (2mm Thick)',
            'PVC Surface J.Box 20mm 4way', 'PVC Surface J.Box 25mm 4way', 'PVC Surface J.Box 32mm 4way',
            'PVC Deep J.Box 20mm 4way', 'PVC Deep J.Box 25mm 4way', 'PVC Deep J.Box 32mm 4way'
        ]

        # 1. Master Items
        for item_name in ITEMS:
            MasterItem.objects.create(name=item_name)
        
        # 2. Company Profile
        profile = CompanyProfile.get_solo()
        profile.name = 'ATUL INDUSTRIES'
        profile.address = 'F-04, Site-C, Surajpur Indl. Area'
        profile.city = 'Greater Noida'
        profile.state = 'Uttar Pradesh'
        profile.pin = '201306'
        profile.gstin = '09BCSPS5065G1ZX'
        profile.phone = '+91 93112 02798'
        profile.email = 'info@atulpipes.com'
        profile.bank = 'Kotak Mahindra Bank'
        profile.account = '9446386730'
        profile.ifsc = 'KKBK0005043'
        profile.branch = 'Ithaira Greater Noida UP'
        profile.defaultTerms = '1. Price: Ex-Unit\n2. Payment: 100% Advance\n3. Freight: FoR Destination\n4. Delivery: 2-3 Working Days\n5. Validity: 7 Days from PI Date\n6. GST @ 18% Extra as Applicable'
        profile.pipePacking = {}
        profile.save()

        # 3. Salesperson
        for sp_data in SEED['sp']:
            Salesperson.objects.create(
                id=sp_data['id'],
                name=sp_data['name'],
                phone=sp_data['phone'],
                email=sp_data['email'],
            )

        # 4. Party
        for p_data in SEED['parties']:
            sp = Salesperson.objects.get(id=p_data['spId'])
            Party.objects.create(
                id=p_data['id'],
                spId=sp,
                name=p_data['name'],
                contact=p_data.get('contact', ''),
                city=p_data['city'],
                state=p_data['state'],
                gstin=p_data['gstin'],
                address=p_data['address'],
                phone=p_data['phone'],
                email=p_data['email'],
            )
        
        # 5. Proformas & Items
        for pf_data in SEED['proformas']:
            party = Party.objects.get(id=pf_data['partyId'])
            sp = Salesperson.objects.get(id=pf_data['spId'])
            
            valid_till = parse_date(pf_data['validTill']) if pf_data['validTill'] else None
            
            pf = ProformaInvoice.objects.create(
                id=pf_data['id'],
                partyId=party,
                spId=sp,
                number=pf_data['number'],
                date=parse_date(pf_data['date']),
                validTill=valid_till,
                subject=pf_data['subject'],
                notes=pf_data['notes'],
                discount=pf_data['discount'],
                showDiscInPDF=pf_data['showDiscInPDF'],
                freight=pf_data.get('freight', 0),
                subtotal=pf_data['subtotal'],
                gstAmt=pf_data['gstAmt'],
                grandTotal=pf_data['grandTotal'],
                shipTo=pf_data['shipTo']
            )

            for item_data in pf_data['items']:
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
                    narration=item_data['narration']
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
