from .webhooks import webhook
from django.urls import path
from . import views

urlpatterns = [
    path('wh/', webhook, name='webhook'),
    path('', views.sec_checkout, name='sec_checkout'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('checkout_successful/<order_nr>', views.checkout_successful, name='checkout_successful')
]
