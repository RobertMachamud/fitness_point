from django.urls import path
from . import views

urlpatterns = [
    path('', views.sec_checkout, name='sec_checkout'),
    path('checkout_successful/<order_number>', views.sec_checkout, name='checkout_successful')
]
