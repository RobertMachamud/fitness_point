from django.urls import path
from . import views

urlpatterns = [
    path('', views.to_cart, name='to_cart'),
]
