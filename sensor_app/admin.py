from django.contrib import admin

# Register your models here.
from .models import Sensor, LiveSensor, Location, UserLogs, UserInteraction
admin.site.register(Sensor)
admin.site.register(LiveSensor)
admin.site.register(Location)
admin.site.register(UserLogs)
admin.site.register(UserInteraction)
