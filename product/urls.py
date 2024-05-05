from django.urls import path
from .views import Createorder, Manage_purchase_order, Acknowledgeorder, Record
 

urlpatterns = [
  path('purchase_orders/', Createorder.as_view(), name='purchase_order_create'),
  path('purchase_orders/<int:po_id>/', Manage_purchase_order.as_view(), name='purchase_order_manage'),
  path('purchase_orders/<int:po_id>/acknowledge/', Acknowledgeorder.as_view(), name='purchase_order_acknowledge'),
  path('vendors/<int:vendor_id>/performance/', Record.as_view(), name='vendor_performance_record'),
 ]