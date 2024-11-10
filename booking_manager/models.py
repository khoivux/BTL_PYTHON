from django.db import models
from homestay_manager.models import Homestay, Service 
# Create your models here.
class Booking(models.Model):
    id = models.BigAutoField(primary_key=True)
    booking_time = models.DateTimeField()
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    status = models.CharField(max_length=255)
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)
    # user = models.ForeignKey(Users, on_delete=models.CASCADE) # type: inore

class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
