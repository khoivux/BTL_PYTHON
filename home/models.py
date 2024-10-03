from django.db import models

# Create your models here.
# models.py
from django.db import models

class Province(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Homestay(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    address = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=5, decimal_places=1)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='homestays')

    def __str__(self):
        return self.name
