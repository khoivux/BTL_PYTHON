from django.contrib import admin
from .models import Province, HomestayFacility, RoomFacility, Service, Homestay, Room
# Register your models here.
admin.site.register(Province)
admin.site.register(HomestayFacility)
admin.site.register(RoomFacility)
admin.site.register(Service)
admin.site.register(Homestay)
admin.site.register(Room)
