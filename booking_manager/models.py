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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bills', null=True, blank=True)
    bill_info = models.JSONField(default=dict)
    
    def get_amount(self):
        """
        Tính tổng doanh thu cho một booking từ các dịch vụ liên quan.
        """
        total_amount = sum([booking_service.service.price for booking_service in self.bookingservice_set.all()])
        return total_amount

    def __str__(self):
        return f"Booking {self.id} - {self.status} for {self.homestay.name}"
class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking {self.booking.id} - Service: {self.service.name}"