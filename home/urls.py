
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.get_home,name='home'), #nếu không có / thì sẽ gọi đến get_home trong views
    path('search', views.search_view, name='search'), # gọi đến hàm search_view trong file views
]  