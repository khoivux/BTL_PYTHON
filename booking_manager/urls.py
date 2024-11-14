
from django.urls import path,include
from . import views
app_name = 'booking_manager'
urlpatterns = [
    path('',views.create_booking,name='booking'),
    path('pay/', views.payment, name = 'pay'),
]  