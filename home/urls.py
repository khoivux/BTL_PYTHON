
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.get_home,name='home'),
    path('search', views.search_view, name='search'),
    path('product/<int:id>/', views.product_detail, name='product'),
]  