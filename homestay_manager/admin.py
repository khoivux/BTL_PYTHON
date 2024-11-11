from django.contrib import admin
from .models import Province, Service, Homestay, Room, HomestayFacilities, HomestayRoom

admin.site.register(Province)
class FacilityInline(admin.TabularInline):
    model = Homestay.facilities.through  

class ServiceInline(admin.TabularInline):
    model = Homestay.services.through  

class HomestayRoomInline(admin.TabularInline):
    model = HomestayRoom  
    extra = 1  


@admin.register(Homestay)
class HomestayAdmin(admin.ModelAdmin):# Loại bỏ trường facilities mặc định để tránh trùng lặp
    inlines = [FacilityInline, ServiceInline, HomestayRoomInline]
    exclude = ('facilities', 'services')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)

@admin.register(HomestayFacilities)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', )

