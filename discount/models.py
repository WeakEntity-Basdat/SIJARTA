from django.db import models

class Voucher(models.Model):
    code = models.CharField(max_length=10)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_days = models.IntegerField()
    usage_quota = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Promo(models.Model):
    code = models.CharField(max_length=10)
    end_date = models.DateField()
