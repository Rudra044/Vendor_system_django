from rest_framework import serializers
from .models import Vendor


class Vendorserializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [ "vendor_code", "name", "contact_details", "address", "password"]

class Vendorsserializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["name", "contact_details", "address"]


class Detailsserializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"



