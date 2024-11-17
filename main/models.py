from django.db import models
from django.contrib.auth.models import User

class ServiceOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField()
    discount_code = models.CharField(max_length=50, blank=True, null=True)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)

    def __str__(self):
        return f"Order by {self.user.username} on {self.order_date}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ServiceSession(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subcategory = models.ForeignKey(Subcategory, related_name='sessions', on_delete=models.CASCADE)

    def __str__(self):
        return self.name