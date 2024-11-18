from django.urls import path
from . import views
from booking_manager.models import Booking

urlpatterns = [
    path('', views.getProfile, name='profile'),
    path('edit/',views.edit, name = 'edit-profile'),
    path('invoices/',views.user_invoices, name = 'invoices'),
    path('xoa-hoa-don/',views.delete, name = "delete"),
]