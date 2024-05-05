import random
from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Purchase, Miscellaneous, Historicalrecord
from .serializers import (Purchase_order, Purchase_order_details,
                           Purchase_order_update, Historicaldataserializer)
from vendor.models import Vendor


class Createorder(APIView):
    def post(self, request):
        serializer = Purchase_order(data=request.data)
        if serializer.is_valid():
            vendor_id = request.data.get("vendor_id")
            vendor = get_object_or_404(Vendor, id=vendor_id)
            po_number = random.randint(0,99999)
            order_date = timezone.now()
            issue_date = order_date
            delivery_date = timezone.now() + timedelta(days=5)
            po_number=po_number
            purchase_order = serializer.save(vendor_id=vendor_id, order_date=order_date, 
                                issue_date=issue_date,delivery_date=delivery_date, po_number=po_number)
            try:
                details = Miscellaneous.objects.get(vendor=vendor)
            except Miscellaneous.DoesNotExist:
                details = Miscellaneous.objects.create(vendor=vendor)
            details.total_order = details.total_order + 1
            details.save()
            response_data = {
                'id':purchase_order.id,
                'data':serializer.data,
                "po_number": po_number
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        vendor_id = request.data.get("vendor_id")
        po = Purchase.objects.all()
        serializer = Purchase_order_details(po, many=True)
        if vendor_id:
            po = Purchase.objects.filter(vendor_id=vendor_id)
            serializer = Purchase_order_details(po, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class Manage_purchase_order(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, po_id):
        vendor = request.user
        po = get_object_or_404(Purchase, id=po_id, vendor=vendor)
        serializer = Purchase_order_update(po, data=request.data)
        if serializer.is_valid():
            po = serializer.save()
            if serializer.data.get("status")=="COMPLETED":
                try:
                    details = Miscellaneous.objects.get(vendor=vendor)
                except Miscellaneous.DoesNotExist:
                    return Response({"message": "Cannot update status"}, status=status.HTTP_200_OK)   
                details.completed_order = details.completed_order + 1
                if timezone.now()<po.delivery_date:
                    details.on_time = details.on_time + 1
                if serializer.data.get("quality_rating")<10:
                    details.total_quality_points =  details.total_quality_points + serializer.data.get("quality_rating")
                else:
                    return Response({"message":"you need  to provide quality rating between 0 to 10"})
                details.save()
                fulfillment_rate = details.completed_order/details.total_order
                vendor.on_time_delivery_rate = details.on_time/details.total_order
                vendor.fulfillment_rate = fulfillment_rate
                vendor.quality_rating_avg= details.total_quality_points/details.completed_order
                vendor.save()
                po.delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self,request, po_id):
        po =  get_object_or_404(Purchase, id=po_id)
        serializer = Purchase_order_details(po)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self,request, po_id):
        po =  get_object_or_404(Vendor, id=po_id)
        po.delete()
        return Response({"message": "purchase_order deleted"}, status=status.HTTP_200_OK)
    

class Acknowledgeorder(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, po_id):
        vendor = request.user
        po = get_object_or_404(Purchase, id=po_id, vendor=vendor)
        try:
            details = Miscellaneous.objects.get(vendor=vendor)
        except Miscellaneous.DoesNotExist:
            return Response({"message": "Cannot update status"}, status=status.HTTP_200_OK)   
        po.acknowledgment_date=timezone.now()
        acknowledge_time = (timezone.now() - po.issue_date).total_seconds() 
        details.total_response_time = acknowledge_time + details.total_response_time 
        vendor.average_response_time = details.total_response_time/details.total_order
        po.save()
        details.save()
        vendor.save()
        return Response({"message":"your details are updated"}, status=status.HTTP_200_OK)
    

class Record(APIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        try:
            details = Historicalrecord.objects.get(vendor=vendor)
        except Historicalrecord.DoesNotExist:
            details = Historicalrecord.objects.create(vendor=vendor, date=datetime.now())
        details.on_time_delivery_rate = vendor.on_time_delivery_rate
        details.quality_rating_avg = vendor.quality_rating_avg
        details.average_response_time = vendor.average_response_time
        details.fulfillment_rate = vendor.fulfillment_rate
        details.save()
        serializer = Historicaldataserializer(details)
        return Response(serializer.data)
        




    



       
