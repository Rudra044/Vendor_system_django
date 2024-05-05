from django.urls import path
from .views import Register, Managevendor, Login

urlpatterns = [
    path('vendor/', Register.as_view(), name='register'),
    path('vendor/login/', Login.as_view(), name='login'),
    path('vendor/<int:id>/', Managevendor.as_view(), name='manage_vendor'),
]