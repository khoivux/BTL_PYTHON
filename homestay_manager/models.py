from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
# Create your models here.

class HomestayFacility(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class RoomFacility(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 

class Service(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.BigIntegerField()

    def __str__(self):
        return self.name

class Province(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Homestay(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.BigIntegerField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)] # type: ignore
    )
    address = models.CharField(max_length=255)
    description = models.TextField()
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    facilities = models.ManyToManyField(HomestayFacility, related_name="homestays") # type: ignore
    services = models.ManyToManyField(Service, related_name="homestays") # type: ignore

    def __str__(self):
        return self.name
    
class Room(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.BigIntegerField()
    room_type = models.CharField(max_length=255)
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)
    facilities = models.ManyToManyField(RoomFacility, related_name="rooms")

    def __str__(self):
        return self.name
    
