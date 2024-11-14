from django.db import models
from homestay_manager.models import Homestay, Service 
from django.conf import settings
# Create your models here.
class Booking(models.Model):
    id = models.BigAutoField(primary_key=True)
    booking_time = models.DateTimeField()
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    status = models.CharField(max_length=255)
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bills',null=True, blank=True)
    #lưu thông tin bills
    bill_info = models.JSONField(default=dict)
class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
