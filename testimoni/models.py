from django.db import models
from django.contrib.auth.models import User
from main.models import Subcategory


class Worker(models.Model):
    """
    Model for workers related to service subcategories.
    """
    full_name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(
        Subcategory, related_name='testimoni_workers', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.full_name


class Testimoni(models.Model):
    """
    Model for testimonials from users who have completed service orders.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='testimoni_testimonials'
    )
    subkategori = models.ForeignKey(
        Subcategory, related_name='testimoni_testimonials', on_delete=models.CASCADE
    )
    worker = models.ForeignKey(
        Worker, related_name='testimoni_testimonials', on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateField(auto_now_add=True)
    rating = models.PositiveIntegerField()  # Rating from 1-10
    comment = models.TextField()

    def __str__(self):
        return f"Testimoni by {self.user.username} on {self.date}"
