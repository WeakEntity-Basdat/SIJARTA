from django.db import models

class Voucher(models.Model):
    kode = models.CharField(max_length=10)
    diskon = models.DecimalField(max_digits=10, decimal_places=2)
    jmlhariberlaku = models.IntegerField()
    kuotapenggunaan = models.IntegerField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)

class Promo(models.Model):
    kode = models.CharField(max_length=10)
    tglakhirberlaku = models.DateField()
    diskon = models.DecimalField(max_digits=10, decimal_places=2)
