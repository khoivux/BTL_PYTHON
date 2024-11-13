from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginv, name='login'),
    path('register/',views.register, name = 'register'),
    path('inf/', views.inf, name = 'inf'),
    path('forget-password',views.forget, name = 'forget-password'),
    path('mail/', views.mail, name='mail'),
    path('reset-password/', views.reset_password, name='reset_password'),
]