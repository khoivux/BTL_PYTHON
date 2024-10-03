from django.contrib import admin
from .models import Homestay, Province
# Register your models here.
# admin.site.register(Homestay)
# admin.site.register(Province)

@admin.register(Homestay)
class HomestayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'address','rating', 'province')  # Hiển thị ID và các thông tin khác

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Hiển thị ID và tên của Province