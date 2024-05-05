from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Vendor


class VendorTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.manage_vendor_url = reverse('manage_vendor', args=[1])
        self.vendor_data = {
            'vendor_code': 'vendor1',
            'name': 'Vendor 1',
            'contact_details': '1234567890',
            'address': 'Vendor Address',
            'password': 'password123'
        }
        self.invalid_vendor_data = {
            'vendor_code': 'vendor1',
            'name': 'Vendor 1',
            'contact_details': '1234567890',
            'address': 'Vendor Address',
            'password': ''
        }
        self.login_credentials = {
            'vendor_code': 'vendor1',
            'password': 'password123'
        }
        self.invalid_login_credentials = {
            'vendor_code': 'vendor1',
            'password': 'invalidpassword' 
        }

    def test_register_vendor(self):
        response = self.client.post(self.register_url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_vendor_invalid_data(self):
        response = self.client.post(self.register_url, self.invalid_vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        self.client.post(self.register_url, self.vendor_data, format='json')

        response = self.client.post(self.login_url, self.login_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        self.client.post(self.register_url, self.vendor_data, format='json')

        response = self.client.post(self.login_url, self.invalid_login_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manage_vendor_update(self):
        response = self.client.post(self.register_url, self.vendor_data, format='json')
        vendor_id = response.data['id']
        self.manage_vendor_url = reverse('manage_vendor', args=[vendor_id])

        updated_data = {
            'name': 'Updated Vendor Name',
            'contact_details': '9876543210',
            'address': 'Updated Vendor Address'
        }
        response = self.client.patch(self.manage_vendor_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manage_vendor_delete(self):
        response = self.client.post(self.register_url, self.vendor_data, format='json')
        vendor_id = response.data['id']
        self.manage_vendor_url = reverse('manage_vendor', args=[vendor_id])

        response = self.client.delete(self.manage_vendor_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
