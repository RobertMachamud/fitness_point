from django.urls import path
from . import views

urlpatterns = [
    path('', views.to_cart, name='to_cart'),
    path('add/<item_id>', views.add_item_to_cart, name='add_item_to_cart'),
]
