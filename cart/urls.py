from django.urls import path
from . import views

urlpatterns = [
    path('', views.to_cart, name='to_cart'),
    path('adjust/<item_id>/', views.adj_cart, name='adj_cart'),
    path('remove/<item_id>/', views.rem_from_cart, name='rem_from_cart'),
    path('add/<item_id>/', views.add_item_to_cart, name='add_item_to_cart'),
]
