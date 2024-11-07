from django.contrib import admin

from .models import Booking, BookingService

# Register your models here.

admin.site.register(Booking)
admin.site.register(BookingService)