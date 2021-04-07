from django.urls import path
from . import views

urlpatterns = [
    path('', views.sec_checkout, name='sec_checkout')
]
