from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    location_preference = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    highness_status = models.IntegerField(default=0)  # Scale from 0 (sober) to 10 (very high)
    

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_friend_requests', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} to {self.to_user}"
