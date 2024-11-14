from django.urls import path
from . import views

urlpatterns = [
    path('', views.getProfile, name='profile'),
    path('edit/',views.edit, name = 'edit-profile'),
]