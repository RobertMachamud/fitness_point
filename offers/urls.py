from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_offers, name='offers'),
    path('add_offer/', views.add_offer, name='add_offer'),
    path('<int:offer_id>/', views.offer_details, name='offer_details'),
    path('update_offer/<int:offer_id>/', views.upd_offer, name='upd_offer'),
    path('delete_offer/<int:offer_id>/', views.del_offer, name='del_offer'),
]
