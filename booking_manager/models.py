from django.db import models

# Create your models here.
class Booking(models.Model):
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    booking_time = models.DateTimeField()
    homestay_id = models.BigIntegerField()
    room_id = models.BigIntegerField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"Booking {self.id} - Homestay {self.homestay_id} - Room {self.room_id}"