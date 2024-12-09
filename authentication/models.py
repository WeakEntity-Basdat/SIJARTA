from django.db import models
# from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     USER_TYPE_CHOICES = [
#         ('pengguna', 'Pengguna'),
#         ('pekerja', 'Pekerja')
#     ]

#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     full_name = models.CharField(max_length=100, null=True, blank=True)
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='pengguna')
#     gender = models.CharField(max_length=1, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], null=True, blank=True)
#     phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
#     birthdate = models.DateField(null=True, blank=True)
#     address = models.CharField(max_length=255, null=True, blank=True)
#     # Additional fields for pekerja
#     bank_name = models.CharField(max_length=100, blank=True, null=True)
#     account_number = models.CharField(max_length=50, blank=True, null=True)
#     npwp = models.CharField(max_length=20, blank=True, null=True)
#     photo_url = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.full_name} - {self.user_type}"
