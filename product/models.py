from django.db import models
from vendor.models import Vendor

class Purchase(models.Model):
    PENDING = 'PENDING'
    CANCELLED = 'CANCELLED'
    COMPLETED = 'COMPLETED'
    STATUS = (
        (PENDING, 'PENDING'),
        (CANCELLED, 'CANCELLED'),
        (COMPLETED, 'COMPLETED'),
    )
    po_number = models.CharField(max_length=20,unique=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='po_number')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField(null=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=15, choices=STATUS, default='PENDING')
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)


class Miscellaneous(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    total_order = models.IntegerField(default=0)
    completed_order = models.IntegerField(default=0)
    total_quality_points = models.IntegerField(default=0)
    on_time = models.IntegerField(default=0)
    total_response_time = models.FloatField(default=0)


class Historicalrecord(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)









