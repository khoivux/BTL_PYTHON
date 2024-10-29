from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.admin_view,name='myadmin'), 
]  