from django.test import TestCase
from django.utils import timezone
from .models import Purchase, Miscellaneous, Historicalrecord
from vendor.models import Vendor

class PurchaseModelTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            vendor_code="vendor1",
            name="Test Vendor",
            contact_details="1234567890",
            address="Test Address"
        )

    def test_purchase_creation(self):
        purchase = Purchase.objects.create(
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            quantity=10,
            issue_date=timezone.now(),
        )
        self.assertIsNotNone(purchase)

    def test_miscellaneous_creation(self):
        miscellaneous = Miscellaneous.objects.create(
            vendor=self.vendor
        )
        self.assertIsNotNone(miscellaneous)

    def test_historical_record_creation(self):
        historical_record = Historicalrecord.objects.create(
            vendor=self.vendor,
            date=timezone.now()
        )
        self.assertIsNotNone(historical_record)
