from django.contrib import admin
from .models import Province, Service, Homestay, Room, HomestayFacilities, HomestayRoom
import matplotlib.pyplot as plt
import io
import base64
from django.utils.safestring import mark_safe
from datetime import datetime
import numpy as np
from django.urls import path
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import openpyxl
from openpyxl.styles import Alignment, Font


# Register models
admin.site.register(Province)

class FacilityInline(admin.TabularInline):
    model = Homestay.facilities.through

class ServiceInline(admin.TabularInline):
    model = Homestay.services.through

class HomestayRoomInline(admin.TabularInline):
    model = HomestayRoom
    extra = 1

@admin.register(Homestay)
class HomestayAdmin(admin.ModelAdmin):
    inlines = [FacilityInline, ServiceInline, HomestayRoomInline]
    exclude = ('facilities', 'services')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(HomestayFacilities)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)

