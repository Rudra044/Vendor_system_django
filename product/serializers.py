from rest_framework import serializers
from .models import Purchase, Historicalrecord

class Purchase_order(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ["vendor_id", "quantity"]


class Purchase_order_details(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


class Purchase_order_update(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ["status", "quality_rating"]

class Historicaldataserializer(serializers.ModelSerializer):
    class Meta:
        model = Historicalrecord
        fields = "__all__"

