from django.db import models
import time
import uuid
from user_app.models import User

# Create your models here.
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locId = models.CharField(default=('LOC' + str(uuid.uuid4().int)[:5]), editable=False, unique=True, max_length=50)
    name = models.CharField(max_length=100, default="Name")
    location = models.CharField(max_length=100, default="Location")
    userName = models.CharField(max_length=100, default="Default User")

    def __str__(self):
        return f"{self.name} ({self.user.name})"



from django.conf import settings

class Sensor(models.Model):
    location = models.ForeignKey('Location', related_name='sensors', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_sensors',  # This enables user.assigned_sensors.all()
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    sensor_id = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.sensor_id})"

class LiveSensor(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='live_sensors', on_delete=models.CASCADE)
    data = models.CharField(max_length=100, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)    
    
class UserLogs(models.Model):
    userName = models.CharField(max_length=100, blank=False, null=False, default="Default User")
    data = models.CharField(max_length=100, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    isSeen = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name
    
class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=True)
    time = models.CharField(default="0", max_length=1000)

    def __str__(self):
        return self.user.name