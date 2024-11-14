from django.db import models


from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)  # Thêm trường số điện thoại
    gender = models.CharField(max_length=10, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')], default='Nam')
    address = models.CharField(max_length=255, blank=True)
    dob = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.user.first_name
