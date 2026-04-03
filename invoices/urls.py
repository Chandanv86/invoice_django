from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    home_view, SalespersonViewSet, PartyViewSet, ProformaInvoiceViewSet,
    CompanyProfileViewSet, PriceListEntryViewSet, MasterItemViewSet,
    sync_db
)

router = DefaultRouter()
router.register(r'salespersons', SalespersonViewSet)
router.register(r'parties', PartyViewSet)
router.register(r'proformas', ProformaInvoiceViewSet)
router.register(r'pricelist', PriceListEntryViewSet)
router.register(r'masteritems', MasterItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/company/', CompanyProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='company-profile'),
    path('api/sync/', sync_db, name='sync-db'),
    path('', home_view, name='home'),
]
