from django.db import models

# Create your models here.
# models.py
class Homestay(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=100)
    rate = models.IntegerField()
    
    def __str__(self):
        return self.name
