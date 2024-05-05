from django.urls import path
from .views import Register, Managevendor, Login

urlpatterns = [
    path('vendor/', Register.as_view()),
    path('vendor/login', Login.as_view()),
    path('vendor/<int:id>', Managevendor.as_view()),
]