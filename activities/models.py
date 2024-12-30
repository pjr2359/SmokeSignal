from django.db import models
from users.models import CustomUser

class Activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    strain_name = models.CharField(max_length=100, blank=True, null=True)
    strain_type = models.CharField(max_length=50, choices=[('indica', 'Indica'), ('sativa', 'Sativa'), ('hybrid', 'Hybrid')])
    rating = models.IntegerField()
    location = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)