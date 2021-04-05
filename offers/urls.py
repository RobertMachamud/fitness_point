from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_offers, name='offers'),
    path('<offer_id>', views.offer_details, name='offer_details'),
]
