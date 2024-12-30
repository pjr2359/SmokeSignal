from django.db import migrations, models
from users.models import CustomUser

class Activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    strain_name = models.CharField(max_length=100, blank=True, null=True)
    strain_type = models.CharField(max_length=50, choices=[('indica', 'Indica'), ('sativa', 'Sativa'), ('hybrid', 'Hybrid')])
    rating = models.IntegerField()
    location = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)  # Verify this exists
    longitude = models.FloatField(null=True, blank=True) # Verify this exists
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_activity_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]