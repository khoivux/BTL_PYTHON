
from django.db import models
from datetime import datetime

class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Province(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class HomestayFacilities(models.Model):
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

class Homestay(models.Model):
    id = models.BigAutoField(primary_key=True)
    address = models.CharField(max_length=255)
    description = models.TextField()
    name = models.CharField(max_length=255)
    number_of_rooms = models.BigIntegerField()
    capacity = models.IntegerField()
    price = models.BigIntegerField()
    rating = models.BigIntegerField()
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    facilities = models.ManyToManyField(HomestayFacilities)
    services = models.ManyToManyField(Service)
    rooms = models.ManyToManyField(Room, through='HomestayRoom', related_name='homestays')
    image = models.ImageField(upload_to='homestay_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class HomestayRoom(models.Model):
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.homestay.name} - {self.room.name} ({self.quantity})"

class Transaction(models.Model):
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.today)  # Sử dụng datetime.today() để lấy ngày hiện tại
    time = models.TimeField(default=datetime.now)  # Để lấy giờ hiện tại

    @staticmethod
    def total_revenue_for_month(year, month):
        transactions = Transaction.objects.filter(date__year=year, date__month=month)
        return sum(transaction.amount for transaction in transactions)

    def __str__(self):
        return f'{self.homestay.name} - {self.amount}'