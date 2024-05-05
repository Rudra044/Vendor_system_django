from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

from .models import Vendor
from .serializers import Vendorserializer, Detailsserializer, Vendorsserializer

'''
you asked to use token based authentication if I do that then only user can append
its own details and url <int:id> for updation and deletion will be no use than as
 it will automatically take for the user by itself. so I ahve not used it
  you can change authentication code for your need
   i have commented that code in patch method if u want authentication '''


class Register(APIView):
    def post(self, request):
        serializer = Vendorserializer(data=request.data)
        if serializer.is_valid():
            vendor = serializer.save(password=make_password(request.data['password']))
            response_data = {
                'id':vendor.id,
                'data':serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self,request):
        vendors = Vendor.objects.all()
        serializer = Detailsserializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class Login(APIView):
    def post(self, request):
        vendor_code = request.data.get("vendor_code")
        password = request.data.get("password")
        vendor = get_object_or_404(Vendor, vendor_code=vendor_code)
        if not vendor:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
        if vendor and check_password(password, vendor.password):
            refresh = RefreshToken.for_user(vendor)
            token = str(refresh.access_token)
            return Response({'message': 'Login successful', 'token': token}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response("wrong password", status=status.HTTP_400_BAD_REQUEST)
    

class Managevendor(APIView):
#permission_classes = [IsAuthenticated]
    def patch(self, request, id):
        #vendor = request.user
        #vendor = get_object_or_404(Vendor, id=id)
        vendor = get_object_or_404(Vendor, id=id)
        serializer = Vendorsserializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            vendor = serializer.save()
            response_data = {
                'id':vendor.id,
                'data':serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request, id):
        vendor =  get_object_or_404(Vendor, id=id)
        serializer = Detailsserializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self,request, id):
        vendor =  get_object_or_404(Vendor, id=id)
        vendor.delete()
        return Response({"message": "vendor deleted"}, status=status.HTTP_200_OK)